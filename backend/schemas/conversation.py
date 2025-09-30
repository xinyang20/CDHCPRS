"""
对话相关的 Pydantic Schemas
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ConversationBase(BaseModel):
    """对话基础 Schema"""
    title: str = Field(..., min_length=1, max_length=200, description="对话标题")


class ConversationCreate(ConversationBase):
    """对话创建 Schema"""
    pass


class ConversationUpdate(BaseModel):
    """对话更新 Schema"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="对话标题")
    is_active: Optional[bool] = Field(None, description="是否激活")


class ConversationResponse(ConversationBase):
    """对话响应 Schema"""
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

