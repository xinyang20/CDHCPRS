"""
用户相关的 Pydantic Schemas
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """用户基础 Schema"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")


class UserCreate(UserBase):
    """用户创建 Schema"""
    password: str = Field(..., min_length=6, max_length=100, description="密码")


class UserLogin(BaseModel):
    """用户登录 Schema"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class UserUpdate(BaseModel):
    """用户更新 Schema"""
    password: Optional[str] = Field(None, min_length=6, max_length=100, description="新密码")
    is_banned: Optional[bool] = Field(None, description="是否封禁")


class UserResponse(UserBase):
    """用户响应 Schema"""
    id: int
    role: str
    is_banned: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token Schema"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token 数据 Schema"""
    username: Optional[str] = None

