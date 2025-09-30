"""
对话管理服务模块
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from models.conversation import Conversation
from models.message import Message
from models.user import User


def create_conversation(db: Session, user: User, title: str) -> Conversation:
    """
    创建新对话
    
    Args:
        db: 数据库会话
        user: 用户对象
        title: 对话标题
        
    Returns:
        创建的对话对象
    """
    conversation = Conversation(
        user_id=user.id,
        title=title,
        is_active=True
    )
    
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    return conversation


def get_user_conversations(db: Session, user: User) -> List[Conversation]:
    """
    获取用户的所有对话
    
    Args:
        db: 数据库会话
        user: 用户对象
        
    Returns:
        对话列表
    """
    conversations = db.query(Conversation)\
        .filter(Conversation.user_id == user.id)\
        .order_by(Conversation.created_at.desc())\
        .all()
    
    return conversations


def get_conversation_by_id(db: Session, conversation_id: int, user: User) -> Conversation:
    """
    根据 ID 获取对话
    
    Args:
        db: 数据库会话
        conversation_id: 对话 ID
        user: 用户对象
        
    Returns:
        对话对象
        
    Raises:
        HTTPException: 对话不存在或无权访问
    """
    conversation = db.query(Conversation)\
        .filter(Conversation.id == conversation_id)\
        .first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="对话不存在"
        )
    
    if conversation.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问此对话"
        )
    
    return conversation


def get_conversation_messages(db: Session, conversation_id: int, user: User) -> List[Message]:
    """
    获取对话的所有消息
    
    Args:
        db: 数据库会话
        conversation_id: 对话 ID
        user: 用户对象
        
    Returns:
        消息列表
    """
    # 先验证对话权限
    conversation = get_conversation_by_id(db, conversation_id, user)
    
    messages = db.query(Message)\
        .filter(Message.conversation_id == conversation.id)\
        .order_by(Message.created_at.asc())\
        .all()
    
    return messages


def create_message(db: Session, conversation_id: int, role: str, content: str) -> Message:
    """
    创建新消息
    
    Args:
        db: 数据库会话
        conversation_id: 对话 ID
        role: 角色 (user/assistant)
        content: 消息内容
        
    Returns:
        创建的消息对象
    """
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return message


def delete_conversation(db: Session, conversation_id: int, user: User) -> None:
    """
    删除对话
    
    Args:
        db: 数据库会话
        conversation_id: 对话 ID
        user: 用户对象
    """
    conversation = get_conversation_by_id(db, conversation_id, user)
    
    db.delete(conversation)
    db.commit()

