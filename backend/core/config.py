"""
应用配置模块
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置类"""

    # 服务器配置
    BACKEND_HOST: str = "127.0.0.1"
    BACKEND_PORT: int = 8001

    # 数据库配置
    DATABASE_URL: str = "sqlite:///./cdhcprs.db"

    # JWT 配置
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 应用配置
    APP_NAME: str = "慢性病诊疗方案推荐系统"
    DEBUG: bool = True

    class Config:
        env_file = "../.env"  # 从项目根目录读取 .env 文件
        case_sensitive = True
        extra = "ignore"  # 忽略 .env 中未定义的字段（如前端配置）


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()

