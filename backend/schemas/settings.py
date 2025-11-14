"""
系统设置相关的 Pydantic Schemas
"""
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator


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
    large_font_scale: float = Field(default=1.5, description="大字版字体放大倍率")


class AdminSettings(BaseModel):
    """管理员设置 Schema（包含所有设置）"""

    website_name: str = Field(default="", description="网站名称")
    website_logo: str = Field(default="", description="网站 Logo URL")
    system_prompt: str = Field(default="", description="系统提示词")
    llm_provider: str = Field(default="", description="LLM 供应商")
    llm_base_url: str = Field(default="", description="LLM 基础 URL")
    llm_api_key: str = Field(default="", description="LLM API Key")
    llm_model_id: str = Field(default="", description="LLM 模型 ID")
    llm_model_name: str = Field(default="", description="LLM 模型名称（用于展示或备用）")
    large_font_scale: float = Field(default=1.5, description="大字版字体放大倍率")

    # 推荐问题配置
    suggested_questions_enabled: str = Field(default="false", description="是否启用推荐问题功能")
    suggested_questions_provider: str = Field(default="", description="推荐问题 LLM 供应商")
    suggested_questions_base_url: str = Field(default="", description="推荐问题 LLM 基础 URL")
    suggested_questions_api_key: str = Field(default="", description="推荐问题 LLM API Key")
    suggested_questions_model_id: str = Field(default="", description="推荐问题 LLM 模型 ID")
    suggested_questions_system_prompt: str = Field(default="", description="推荐问题系统提示词")
    suggested_questions_count: str = Field(default="3", description="推荐问题数量")
    suggested_questions_max_rounds: str = Field(default="5", description="最大消息轮数")
    suggested_questions_template_questions: str = Field(default="[]", description="模板问题（JSON 数组）")


class AdminSettingsUpdate(BaseModel):
    """管理员设置更新 Schema"""

    website_name: Optional[str] = Field(None, description="网站名称")
    website_logo: Optional[str] = Field(None, description="网站 Logo URL")
    system_prompt: Optional[str] = Field(None, description="系统提示词")
    llm_provider: Optional[str] = Field(None, description="LLM 供应商")
    llm_base_url: Optional[str] = Field(None, description="LLM 基础 URL")
    llm_api_key: Optional[str] = Field(None, description="LLM API Key")
    llm_model_id: Optional[str] = Field(None, description="LLM 模型 ID")
    llm_model_name: Optional[str] = Field(None, description="LLM 模型名称（用于展示或备用）")
    large_font_scale: Optional[float] = Field(None, description="大字版字体放大倍率")

    # 推荐问题配置
    suggested_questions_enabled: Optional[str] = Field(None, description="是否启用推荐问题功能")
    suggested_questions_provider: Optional[str] = Field(None, description="推荐问题 LLM 供应商")
    suggested_questions_base_url: Optional[str] = Field(None, description="推荐问题 LLM 基础 URL")
    suggested_questions_api_key: Optional[str] = Field(None, description="推荐问题 LLM API Key")
    suggested_questions_model_id: Optional[str] = Field(None, description="推荐问题 LLM 模型 ID")
    suggested_questions_system_prompt: Optional[str] = Field(None, description="推荐问题系统提示词")
    suggested_questions_count: Optional[str] = Field(None, description="推荐问题数量")
    suggested_questions_max_rounds: Optional[str] = Field(None, description="最大消息轮数")
    suggested_questions_template_questions: Optional[str] = Field(None, description="模板问题（JSON 数组）")


class TestConnectionRequest(BaseModel):
    """测试连接请求 Schema"""

    llm_provider: str = Field(..., description="LLM 供应商")
    llm_api_key: str = Field(..., description="LLM API Key")
    llm_model_id: Optional[str] = Field(None, description="LLM 模型 ID")
    llm_model_name: Optional[str] = Field(None, description="LLM 模型名称")
    llm_base_url: Optional[str] = Field(None, description="LLM 基础 URL（可选）")

    @model_validator(mode="after")
    def validate_identifier(cls, values):
        if not (values.llm_model_id or values.llm_model_name):
            raise ValueError("llm_model_id 或 llm_model_name 至少需要填写一个")
        return values


class TestConnectionResponse(BaseModel):
    """测试连接响应 Schema"""

    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")


class ModelOption(BaseModel):
    """可选模型 Schema"""

    id: str = Field(..., description="模型 ID")
    name: Optional[str] = Field(None, description="模型名称")
    owned_by: Optional[str] = Field(None, description="模型归属")


class ModelListResponse(BaseModel):
    """模型列表响应 Schema"""

    models: List[ModelOption] = Field(..., description="模型列表")


class ModelListRequest(BaseModel):
    """模型列表请求 Schema"""

    llm_provider: str = Field(..., description="LLM 供应商")
    llm_api_key: str = Field(..., description="LLM API Key")
    llm_base_url: Optional[str] = Field(None, description="LLM 基础 URL（可选）")


class LogoUploadResponse(BaseModel):
    """Logo 上传响应 Schema"""

    logo_url: str = Field(..., description="Logo 的 Data URL（Base64 编码）")


