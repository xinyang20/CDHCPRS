"""
系统设置相关的 Pydantic Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional


class SystemSettingBase(BaseModel):
    """系统设置基础 Schema"""
    key: str = Field(..., description="设置键")
    value: str = Field(..., description="设置值")


class SystemSettingResponse(SystemSettingBase):
    """系统设置响应 Schema"""
    
    class Config:
        from_attributes = True


class PublicSettings(BaseModel):
    """公共设置 Schema（不包含敏感信息）"""
    website_name: str = Field(..., description="网站名称")
    website_logo: str = Field(..., description="网站 Logo URL")


class AdminSettings(BaseModel):
    """管理员设置 Schema（包含所有设置）"""
    website_name: str = Field(..., description="网站名称")
    website_logo: str = Field(..., description="网站 Logo URL")
    system_prompt: str = Field(..., description="系统提示词")
    llm_provider: str = Field(..., description="LLM 供应商")
    llm_api_key: str = Field(..., description="LLM API Key")
    llm_model_id: str = Field(..., description="LLM 模型 ID")


class AdminSettingsUpdate(BaseModel):
    """管理员设置更新 Schema"""
    website_name: Optional[str] = Field(None, description="网站名称")
    website_logo: Optional[str] = Field(None, description="网站 Logo URL")
    system_prompt: Optional[str] = Field(None, description="系统提示词")
    llm_provider: Optional[str] = Field(None, description="LLM 供应商")
    llm_api_key: Optional[str] = Field(None, description="LLM API Key")
    llm_model_id: Optional[str] = Field(None, description="LLM 模型 ID")


class TestConnectionRequest(BaseModel):
    """测试连接请求 Schema"""
    llm_provider: str = Field(..., description="LLM 供应商")
    llm_api_key: str = Field(..., description="LLM API Key")
    llm_model_id: str = Field(..., description="LLM 模型 ID")


class TestConnectionResponse(BaseModel):
    """测试连接响应 Schema"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")

