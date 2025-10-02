"""
对话路由
"""
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
from services.llm import stream_llm_response

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

