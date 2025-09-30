"""
数据库初始化脚本
创建所有表并插入默认数据
"""
from core.database import engine, Base, SessionLocal
from models import User, SystemSetting
import bcrypt


def hash_password(password: str) -> str:
    """哈希密码"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def init_database():
    """初始化数据库"""
    print("开始初始化数据库...")
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("✓ 数据库表创建成功")
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 检查是否已有管理员账户
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            # 创建默认管理员账户
            hashed_password = hash_password("admin123")
            admin = User(
                username="admin",
                hashed_password=hashed_password,
                role="admin",
                is_banned=False
            )
            db.add(admin)
            print("✓ 默认管理员账户创建成功 (用户名: admin, 密码: admin123)")
        else:
            print("✓ 管理员账户已存在")
        
        # 设置默认系统配置
        default_settings = {
            "website_name": "慢性病诊疗方案推荐系统",
            "website_logo": "",
            "system_prompt": "你是一位专业的中医医生，擅长诊断和治疗各种慢性病。请根据患者提供的信息，给出专业的诊疗建议。",
            "llm_provider": "deepseek",
            "llm_api_key": "",
            "llm_model_id": "deepseek-chat",
        }
        
        for key, value in default_settings.items():
            setting = db.query(SystemSetting).filter(SystemSetting.key == key).first()
            if not setting:
                setting = SystemSetting(key=key, value=value)
                db.add(setting)
        
        print("✓ 默认系统配置设置成功")
        
        # 提交更改
        db.commit()
        print("\n数据库初始化完成！")
        print("\n默认管理员账户信息：")
        print("  用户名: admin")
        print("  密码: admin123")
        print("\n请在生产环境中立即修改默认密码！")
        
    except Exception as e:
        print(f"✗ 初始化失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_database()

