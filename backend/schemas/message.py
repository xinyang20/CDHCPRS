"""
消息相关的 Pydantic Schemas
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class MessageBase(BaseModel):
    """消息基础 Schema"""
    role: str = Field(..., description="角色 (user/assistant)")
    content: str = Field(..., description="消息内容 (Markdown 格式)")


class MessageCreate(BaseModel):
    """消息创建 Schema"""
    content: str = Field(..., min_length=1, description="用户消息内容")
    user_info: Optional[str] = Field(None, description="用户个人信息（可选）")


class MessageResponse(MessageBase):
    """消息响应 Schema"""
    id: int
    conversation_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

