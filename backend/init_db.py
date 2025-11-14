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
    print("[OK] 数据库表创建成功")

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
            print("[OK] 默认管理员账户创建成功 (用户名: admin, 密码: admin123)")
        else:
            print("[OK] 管理员账户已存在")
        
        # 设置默认系统配置
        default_settings = {
            "website_name": "慢性病诊疗方案推荐系统",
            "website_logo": "",
            "system_prompt": "你是一位专业的中医医生，擅长诊断和治疗各种慢性病。请根据患者提供的信息，给出专业的诊疗建议。",
            "llm_provider": "deepseek",
            "llm_base_url": "https://api.deepseek.com/v1",
            "llm_api_key": "",
            "llm_model_id": "deepseek-chat",
            "large_font_scale": "1.5",
            # 推荐问题配置
            "suggested_questions_enabled": "false",
            "suggested_questions_provider": "deepseek",
            "suggested_questions_base_url": "",
            "suggested_questions_api_key": "",
            "suggested_questions_model_id": "",
            "suggested_questions_system_prompt": """你是一个智能助手，负责根据用户的对话历史，推测用户接下来可能想问的问题。

请仔细分析对话内容，生成3个用户可能感兴趣的后续问题。这些问题应该：
1. 与当前对话主题紧密相关
2. 具有延续性和深入性
3. 简洁明了，易于理解

请以 JSON 数组格式返回问题列表，例如：
["问题1", "问题2", "问题3"]

或者使用编号列表格式：
1. 问题1
2. 问题2
3. 问题3""",
            "suggested_questions_count": "3",
            "suggested_questions_max_rounds": "5",
            "suggested_questions_template_questions": '["如何改善症状？", "需要注意什么饮食？", "有什么锻炼建议？", "药物治疗的副作用有哪些？", "病情恢复需要多长时间？"]',
        }
        
        for key, value in default_settings.items():
            setting = db.query(SystemSetting).filter(SystemSetting.key == key).first()
            if not setting:
                setting = SystemSetting(key=key, value=value)
                db.add(setting)
        
        print("[OK] 默认系统配置设置成功")

        # 提交更改
        db.commit()
        print("\n数据库初始化完成！")
        print("\n默认管理员账户信息：")
        print("  用户名: admin")
        print("  密码: admin123")
        print("\n请在生产环境中立即修改默认密码！")

    except Exception as e:
        print(f"[ERROR] 初始化失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_database()

