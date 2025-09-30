"""
数据库连接配置模块
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import get_settings

settings = get_settings()

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite 需要此配置
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()


def get_db():
    """
    获取数据库会话的依赖函数
    用于 FastAPI 的依赖注入
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

