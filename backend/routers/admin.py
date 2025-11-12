"""
管理员路由
"""
from typing import List
import base64
import os

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.conversation import ConversationResponse
from schemas.message import MessageResponse
from schemas.settings import (
    AdminSettings,
    AdminSettingsUpdate,
    ModelListRequest,
    ModelListResponse,
    TestConnectionRequest,
    TestConnectionResponse,
    LogoUploadResponse,
)
from schemas.user import UserResponse, UserUpdate
from services.admin import (
    delete_conversation_by_admin,
    delete_user,
    get_all_conversations,
    get_all_users,
    get_conversation_messages_by_admin,
    update_system_settings_with_model_check,
    update_user_ban_status,
)
from services.auth import get_current_admin_user
from services.llm import list_llm_models, test_llm_connection
from services.settings import get_all_settings, update_setting

router = APIRouter(prefix="/api/admin", tags=["管理员"])


# ========== 用户管理 ==========

@router.get("/users", response_model=List[UserResponse])
def get_users(
    current_admin=Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    获取所有用户列表

    Args:
        current_admin: 当前管理员
        db: 数据库会话

    Returns:
        用户列表
    """

    users = get_all_users(db)
    return users


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_admin=Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    更新用户（封禁/解封）

    Args:
        user_id: 用户 ID
        user_data: 用户更新数据
        current_admin: 当前管理员
        db: 数据库会话

    Returns:
        更新后的用户信息
    """

    if user_data.is_banned is not None:
        user = update_user_ban_status(db, user_id, user_data.is_banned)
        return user

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="未提供可更新的字段",
    )


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(
    user_id: int,
    current_admin=Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    删除用户

    Args:
        user_id: 用户 ID
        current_admin: 当前管理员
        db: 数据库会话
    """

    delete_user(db, user_id)
    return None


# ========== 对话管理 ==========

@router.get("/conversations", response_model=List[ConversationResponse])
def get_conversations(
    current_admin=Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    获取所有对话列表

    Args:
        current_admin: 当前管理员
        db: 数据库会话

    Returns:
        对话列表
    """

    conversations = get_all_conversations(db)
    return conversations


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
def get_conversation_messages(
    conversation_id: int,
    current_admin=Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    管理员查看指定对话的消息记录

    Args:
        conversation_id: 对话 ID
        current_admin: 当前管理员
        db: 数据库会话

    Returns:
        消息列表
    """

    messages = get_conversation_messages_by_admin(db, conversation_id)
    return messages


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(
    conversation_id: int,
    current_admin=Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    删除对话

    Args:
        conversation_id: 对话 ID
        current_admin: 当前管理员
        db: 数据库会话
    """

    delete_conversation_by_admin(db, conversation_id)
    return None


# ========== 系统设置 ==========

@router.get("/settings", response_model=AdminSettings)
def get_settings(
    current_admin=Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    获取所有系统设置

    Args:
        current_admin: 当前管理员
        db: 数据库会话

    Returns:
        系统设置
    """

    settings = get_all_settings(db)

    return AdminSettings(
        website_name=settings.get("website_name", ""),
        website_logo=settings.get("website_logo", ""),
        system_prompt=settings.get("system_prompt", ""),
        llm_provider=settings.get("llm_provider", ""),
        llm_base_url=settings.get("llm_base_url", ""),
        llm_api_key=settings.get("llm_api_key", ""),
        llm_model_id=settings.get("llm_model_id", ""),
        large_font_scale=float(settings.get("large_font_scale", "1.5")),
    )


@router.put("/settings", response_model=AdminSettings)
def update_settings(
    settings_data: AdminSettingsUpdate,
    current_admin=Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    更新系统设置

    Args:
        settings_data: 设置更新数据
        current_admin: 当前管理员
        db: 数据库会话

    Returns:
        更新后的系统设置
    """

    settings_dict = settings_data.model_dump(exclude_none=True)

    # 将 large_font_scale 转换为字符串以存储到数据库
    if "large_font_scale" in settings_dict:
        settings_dict["large_font_scale"] = str(settings_dict["large_font_scale"])

    update_system_settings_with_model_check(db, settings_dict)

    all_settings = get_all_settings(db)

    return AdminSettings(
        website_name=all_settings.get("website_name", ""),
        website_logo=all_settings.get("website_logo", ""),
        system_prompt=all_settings.get("system_prompt", ""),
        llm_provider=all_settings.get("llm_provider", ""),
        llm_base_url=all_settings.get("llm_base_url", ""),
        llm_api_key=all_settings.get("llm_api_key", ""),
        llm_model_id=all_settings.get("llm_model_id", ""),
        large_font_scale=float(all_settings.get("large_font_scale", "1.5")),
    )


@router.post("/settings/test-connection", response_model=TestConnectionResponse)
async def test_connection(
    test_data: TestConnectionRequest,
    current_admin=Depends(get_current_admin_user),
):
    """
    测试大模型连接

    Args:
        test_data: 测试连接数据
        current_admin: 当前管理员

    Returns:
        测试结果
    """

    model_identifier = test_data.llm_model_id or test_data.llm_model_name

    success, message = await test_llm_connection(
        test_data.llm_provider,
        test_data.llm_api_key,
        model_identifier,
        test_data.llm_base_url,
    )

    return TestConnectionResponse(success=success, message=message)


@router.post("/settings/models", response_model=ModelListResponse)
async def fetch_models(
    request: ModelListRequest,
    current_admin=Depends(get_current_admin_user),
):
    """
    获取指定供应商的可用模型列表

    Args:
        request: 模型列表请求参数
        current_admin: 当前管理员

    Returns:
        模型列表
    """

    success, models, error_message = await list_llm_models(
        request.llm_provider,
        request.llm_api_key,
        request.llm_base_url,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message,
        )

    return ModelListResponse(models=models)


@router.post("/settings/upload-logo", response_model=LogoUploadResponse)
async def upload_logo(
    file: UploadFile = File(...),
    current_admin=Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    上传网站 Logo

    Args:
        file: 上传的图片文件
        current_admin: 当前管理员
        db: 数据库会话

    Returns:
        Base64 编码的图片数据
    """

    # 验证文件类型
    allowed_types = ["image/png", "image/jpeg", "image/jpg", "image/gif", "image/svg+xml", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的文件类型。允许的类型: {', '.join(allowed_types)}"
        )

    # 验证文件大小 (2MB)
    content = await file.read()
    if len(content) > 2 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件大小不能超过 2MB"
        )

    # 转换为 Base64
    base64_data = base64.b64encode(content).decode('utf-8')
    data_url = f"data:{file.content_type};base64,{base64_data}"

    # 保存到数据库
    update_setting(db, "website_logo", data_url)

    return LogoUploadResponse(logo_url=data_url)

