"""
系统设置服务模块
"""
from typing import Dict, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.system_setting import SystemSetting


def get_setting(db: Session, key: str) -> Optional[str]:
    """获取单个系统设置"""

    result = db.execute(
        select(SystemSetting).where(SystemSetting.key == key)
    ).scalar_one_or_none()
    return result.value if result else None


def get_all_settings(db: Session) -> Dict[str, str]:
    """获取所有系统设置"""

    results = db.execute(select(SystemSetting)).scalars().all()
    return {setting.key: setting.value for setting in results}


def update_setting(db: Session, key: str, value: str) -> SystemSetting:
    """更新单个系统设置"""

    setting = db.execute(
        select(SystemSetting).where(SystemSetting.key == key)
    ).scalar_one_or_none()

    if setting:
        setting.value = value
    else:
        setting = SystemSetting(key=key, value=value)
        db.add(setting)

    db.commit()
    db.refresh(setting)
    return setting


def update_multiple_settings(db: Session, settings_dict: Dict[str, Optional[str]]) -> None:
    """批量更新系统设置（忽略值为 None 的键）"""

    filtered = {key: value for key, value in settings_dict.items() if value is not None}
    if not filtered:
        return

    existing_settings = db.execute(
        select(SystemSetting).where(SystemSetting.key.in_(filtered.keys()))
    ).scalars().all()
    existing_map = {setting.key: setting for setting in existing_settings}

    for key, value in filtered.items():
        if key in existing_map:
            existing_map[key].value = value
        else:
            db.add(SystemSetting(key=key, value=value))

    db.commit()
