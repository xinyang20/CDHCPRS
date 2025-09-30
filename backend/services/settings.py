"""
系统设置服务模块
"""
from sqlalchemy.orm import Session
from typing import Dict, Optional
from models.system_setting import SystemSetting


def get_setting(db: Session, key: str) -> Optional[str]:
    """
    获取单个系统设置
    
    Args:
        db: 数据库会话
        key: 设置键
        
    Returns:
        设置值，如果不存在返回 None
    """
    setting = db.query(SystemSetting).filter(SystemSetting.key == key).first()
    return setting.value if setting else None


def get_all_settings(db: Session) -> Dict[str, str]:
    """
    获取所有系统设置
    
    Args:
        db: 数据库会话
        
    Returns:
        设置字典
    """
    settings = db.query(SystemSetting).all()
    return {s.key: s.value for s in settings}


def update_setting(db: Session, key: str, value: str) -> SystemSetting:
    """
    更新系统设置
    
    Args:
        db: 数据库会话
        key: 设置键
        value: 设置值
        
    Returns:
        更新后的设置对象
    """
    setting = db.query(SystemSetting).filter(SystemSetting.key == key).first()
    
    if setting:
        setting.value = value
    else:
        setting = SystemSetting(key=key, value=value)
        db.add(setting)
    
    db.commit()
    db.refresh(setting)
    
    return setting


def update_multiple_settings(db: Session, settings_dict: Dict[str, str]) -> None:
    """
    批量更新系统设置
    
    Args:
        db: 数据库会话
        settings_dict: 设置字典
    """
    for key, value in settings_dict.items():
        if value is not None:  # 只更新非 None 的值
            update_setting(db, key, value)

