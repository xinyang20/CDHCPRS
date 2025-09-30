"""
管理员路由
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.user import UserResponse, UserUpdate
from schemas.conversation import ConversationResponse
from schemas.settings import AdminSettings, AdminSettingsUpdate, TestConnectionRequest, TestConnectionResponse
from services.auth import get_current_admin_user
from services.admin import (
    get_all_users, update_user_ban_status, delete_user,
    get_all_conversations, delete_conversation_by_admin,
    update_system_settings_with_model_check
)
from services.settings import get_all_settings
from services.llm import test_llm_connection

router = APIRouter(prefix="/api/admin", tags=["管理员"])


# ========== 用户管理 ==========

@router.get("/users", response_model=List[UserResponse])
def get_users(
    current_admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
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
    current_admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
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
    
    return None


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(
    user_id: int,
    current_admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
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
    current_admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
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


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(
    conversation_id: int,
    current_admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
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
    current_admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
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
        llm_api_key=settings.get("llm_api_key", ""),
        llm_model_id=settings.get("llm_model_id", "")
    )


@router.put("/settings", response_model=AdminSettings)
def update_settings(
    settings_data: AdminSettingsUpdate,
    current_admin = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
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
    # 转换为字典
    settings_dict = settings_data.model_dump(exclude_none=True)
    
    # 更新设置（如果模型配置改变会自动禁用所有对话）
    update_system_settings_with_model_check(db, settings_dict)
    
    # 返回更新后的设置
    all_settings = get_all_settings(db)
    
    return AdminSettings(
        website_name=all_settings.get("website_name", ""),
        website_logo=all_settings.get("website_logo", ""),
        system_prompt=all_settings.get("system_prompt", ""),
        llm_provider=all_settings.get("llm_provider", ""),
        llm_api_key=all_settings.get("llm_api_key", ""),
        llm_model_id=all_settings.get("llm_model_id", "")
    )


@router.post("/settings/test-connection", response_model=TestConnectionResponse)
async def test_connection(
    test_data: TestConnectionRequest,
    current_admin = Depends(get_current_admin_user)
):
    """
    测试大模型连接
    
    Args:
        test_data: 测试连接数据
        current_admin: 当前管理员
        
    Returns:
        测试结果
    """
    success, message = await test_llm_connection(
        test_data.llm_provider,
        test_data.llm_api_key,
        test_data.llm_model_id
    )
    
    return TestConnectionResponse(success=success, message=message)

