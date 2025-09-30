"""
公共路由（无需认证）
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.settings import PublicSettings
from services.settings import get_setting

router = APIRouter(prefix="/api/public", tags=["公共接口"])


@router.get("/settings", response_model=PublicSettings)
def get_public_settings(db: Session = Depends(get_db)):
    """
    获取公共设置（网站名称、Logo 等）
    
    Args:
        db: 数据库会话
        
    Returns:
        公共设置信息
    """
    website_name = get_setting(db, "website_name") or "慢性病诊疗方案推荐系统"
    website_logo = get_setting(db, "website_logo") or ""
    
    return PublicSettings(
        website_name=website_name,
        website_logo=website_logo
    )

