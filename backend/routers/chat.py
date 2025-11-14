"""
对话路由
"""
import json
import random
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.conversation import ConversationCreate, ConversationResponse
from schemas.message import MessageCreate, MessageResponse
from services.auth import get_current_user
from services.chat import (
    create_conversation, get_user_conversations, get_conversation_by_id,
    get_conversation_messages, create_message, delete_conversation
)
from services.settings import get_setting
from services.llm import stream_llm_response, generate_suggested_questions

router = APIRouter(prefix="/api/chat", tags=["对话"])


@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def create_new_conversation(
    conversation_data: ConversationCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    创建新对话
    
    Args:
        conversation_data: 对话创建数据
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        创建的对话信息
    """
    conversation = create_conversation(db, current_user, conversation_data.title)
    return conversation


@router.get("/conversations", response_model=List[ConversationResponse])
def get_conversations(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户的所有对话
    
    Args:
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        对话列表
    """
    conversations = get_user_conversations(db, current_user)
    return conversations


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取指定对话
    
    Args:
        conversation_id: 对话 ID
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        对话信息
    """
    conversation = get_conversation_by_id(db, conversation_id, current_user)
    return conversation


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
def get_messages(
    conversation_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取对话的所有消息
    
    Args:
        conversation_id: 对话 ID
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        消息列表
    """
    messages = get_conversation_messages(db, conversation_id, current_user)
    return messages


@router.post("/conversations/{conversation_id}/messages")
async def send_message(
    conversation_id: int,
    message_data: MessageCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    发送消息并获取流式响应
    
    Args:
        conversation_id: 对话 ID
        message_data: 消息数据
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        流式响应
    """
    # 验证对话权限和状态
    conversation = get_conversation_by_id(db, conversation_id, current_user)
    
    if not conversation.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="系统模型已更新，请开启新的对话"
        )
    
    # 构建用户消息内容
    user_content = message_data.content
    if message_data.user_info:
        user_content = f"[用户信息]\n{message_data.user_info}\n\n[问题]\n{user_content}"
    
    # 保存用户消息
    create_message(db, conversation_id, "user", user_content)
    
    # 获取历史消息
    messages = get_conversation_messages(db, conversation_id, current_user)
    message_history = [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]
    
    # 获取系统设置
    system_prompt = get_setting(db, "system_prompt") or "你是一位专业的中医医生。"
    llm_provider = get_setting(db, "llm_provider") or "deepseek"
    llm_api_key = (get_setting(db, "llm_api_key") or "").strip()
    llm_model_id = (get_setting(db, "llm_model_id") or "").strip()
    llm_model_name = (get_setting(db, "llm_model_name") or "").strip()
    llm_base_url = (get_setting(db, "llm_base_url") or "").strip()

    if not llm_api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="系统未配置 LLM API Key，请联系管理员"
        )

    model_identifier = llm_model_id or llm_model_name or "deepseek-chat"
    base_url = llm_base_url or None

    # 流式生成响应
    async def generate_response():
        full_response = ""

        async for chunk in stream_llm_response(
            provider=llm_provider,
            api_key=llm_api_key,
            model=model_identifier,
            system_prompt=system_prompt,
            messages=message_history,
            base_url=base_url,
        ):
            full_response += chunk
            yield chunk
        
        # 保存助手消息
        create_message(db, conversation_id, "assistant", full_response)
    
    return StreamingResponse(generate_response(), media_type="text/plain")


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conv(
    conversation_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    删除对话

    Args:
        conversation_id: 对话 ID
        current_user: 当前用户
        db: 数据库会话
    """
    delete_conversation(db, conversation_id, current_user)
    return None


@router.get("/conversations/{conversation_id}/suggested-questions")
async def get_suggested_questions_endpoint(
    conversation_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取推荐问题（猜你想问）

    Args:
        conversation_id: 对话 ID
        current_user: 当前用户
        db: 数据库会话

    Returns:
        推荐问题列表
    """
    # 验证对话权限
    conversation = get_conversation_by_id(db, conversation_id, current_user)

    # 检查功能是否启用
    enabled = get_setting(db, "suggested_questions_enabled")
    if enabled != "true":
        return {"questions": []}

    # 获取配置
    count = int(get_setting(db, "suggested_questions_count") or "3")
    max_rounds = int(get_setting(db, "suggested_questions_max_rounds") or "5")

    # 获取历史消息
    messages = get_conversation_messages(db, conversation_id, current_user)

    # 如果没有消息，返回空列表
    if not messages:
        return {"questions": []}

    # 限制消息轮数（按对话轮次计算）
    limited_messages = []
    user_msg_count = 0
    for msg in reversed(messages):
        if msg.role == "user":
            user_msg_count += 1
            if user_msg_count > max_rounds:
                break
        limited_messages.insert(0, msg)

    # 构建消息历史
    message_history = [
        {"role": msg.role, "content": msg.content}
        for msg in limited_messages
    ]

    # 获取推荐问题专用的 LLM 配置
    provider = get_setting(db, "suggested_questions_provider") or get_setting(db, "llm_provider") or "deepseek"
    api_key = (get_setting(db, "suggested_questions_api_key") or get_setting(db, "llm_api_key") or "").strip()
    model_id = (get_setting(db, "suggested_questions_model_id") or get_setting(db, "llm_model_id") or "").strip()
    base_url = (get_setting(db, "suggested_questions_base_url") or get_setting(db, "llm_base_url") or "").strip() or None

    # 默认的系统提示词
    default_prompt = """你是一个智能助手，负责根据用户的对话历史，推测用户接下来可能想问的问题。

请仔细分析对话内容，生成3个用户可能感兴趣的后续问题。这些问题应该：
1. 与当前对话主题紧密相关
2. 具有延续性和深入性
3. 简洁明了，易于理解

请以 JSON 数组格式返回问题列表，例如：
["问题1", "问题2", "问题3"]

或者使用编号列表格式：
1. 问题1
2. 问题2
3. 问题3"""

    system_prompt = get_setting(db, "suggested_questions_system_prompt") or default_prompt

    if not api_key:
        # 如果没有配置 API Key，直接使用模板问题
        template_questions_str = get_setting(db, "suggested_questions_template_questions") or "[]"
        try:
            template_questions = json.loads(template_questions_str)
            if template_questions and len(template_questions) > 0:
                selected = random.sample(template_questions, min(count, len(template_questions)))
                return {"questions": selected}
        except (json.JSONDecodeError, ValueError):
            pass
        return {"questions": []}

    model_identifier = model_id or "deepseek-chat"

    # 调用大模型生成推荐问题（包含重试机制）
    success, questions, error = await generate_suggested_questions(
        provider=provider,
        api_key=api_key,
        model=model_identifier,
        system_prompt=system_prompt,
        messages=message_history,
        count=count,
        base_url=base_url,
        max_retries=1,
    )

    if success and questions:
        return {"questions": questions[:count]}

    # 降级机制：使用模板问题
    template_questions_str = get_setting(db, "suggested_questions_template_questions") or "[]"
    try:
        template_questions = json.loads(template_questions_str)
        if template_questions and len(template_questions) > 0:
            selected = random.sample(template_questions, min(count, len(template_questions)))
            return {"questions": selected}
    except (json.JSONDecodeError, ValueError):
        pass

    # 如果模板问题也没有，返回空列表
    return {"questions": []}

