"""
管理员服务模块
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from models.user import User
from models.conversation import Conversation
from services.settings import update_multiple_settings


def get_all_users(db: Session) -> List[User]:
    """
    获取所有用户
    
    Args:
        db: 数据库会话
        
    Returns:
        用户列表
    """
    users = db.query(User).order_by(User.created_at.desc()).all()
    return users


def update_user_ban_status(db: Session, user_id: int, is_banned: bool) -> User:
    """
    更新用户封禁状态
    
    Args:
        db: 数据库会话
        user_id: 用户 ID
        is_banned: 是否封禁
        
    Returns:
        更新后的用户对象
        
    Raises:
        HTTPException: 用户不存在或不能封禁管理员
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    if user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能封禁管理员账户"
        )
    
    user.is_banned = is_banned
    db.commit()
    db.refresh(user)
    
    return user


def delete_user(db: Session, user_id: int) -> None:
    """
    删除用户
    
    Args:
        db: 数据库会话
        user_id: 用户 ID
        
    Raises:
        HTTPException: 用户不存在或不能删除管理员
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    if user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除管理员账户"
        )
    
    db.delete(user)
    db.commit()


def get_all_conversations(db: Session) -> List[Conversation]:
    """
    获取所有对话
    
    Args:
        db: 数据库会话
        
    Returns:
        对话列表
    """
    conversations = db.query(Conversation)\
        .order_by(Conversation.created_at.desc())\
        .all()
    
    return conversations


def delete_conversation_by_admin(db: Session, conversation_id: int) -> None:
    """
    管理员删除对话
    
    Args:
        db: 数据库会话
        conversation_id: 对话 ID
        
    Raises:
        HTTPException: 对话不存在
    """
    conversation = db.query(Conversation)\
        .filter(Conversation.id == conversation_id)\
        .first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="对话不存在"
        )
    
    db.delete(conversation)
    db.commit()


def disable_all_conversations(db: Session) -> None:
    """
    禁用所有历史对话（模型切换时调用）
    
    Args:
        db: 数据库会话
    """
    db.query(Conversation).update({"is_active": False})
    db.commit()


def update_system_settings_with_model_check(
    db: Session,
    settings_dict: dict
) -> None:
    """
    更新系统设置，如果模型配置改变则禁用所有对话
    
    Args:
        db: 数据库会话
        settings_dict: 设置字典
    """
    # 检查是否更新了模型相关配置
    model_keys = ["llm_provider", "llm_api_key", "llm_model_id"]
    model_changed = any(key in settings_dict for key in model_keys)
    
    # 更新设置
    update_multiple_settings(db, settings_dict)
    
    # 如果模型配置改变，禁用所有对话
    if model_changed:
        disable_all_conversations(db)

