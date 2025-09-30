"""
慢性病诊疗方案推荐系统 - 后端主应用
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, public, chat, admin
from core.config import get_settings

settings = get_settings()

# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    description="基于大语言模型的慢性病诊疗方案推荐系统",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(public.router)
app.include_router(chat.router)
app.include_router(admin.router)


@app.get("/")
def root():
    """根路径"""
    return {
        "message": "欢迎使用慢性病诊疗方案推荐系统 API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/api/health")
def health_check():
    """
    健康检查接口
    用于前端监控后端服务状态
    """
    return {
        "status": "healthy",
        "message": "后端服务运行正常",
        "version": "1.0.0"
    }


def main():
    """主函数（用于 uv 初始化的兼容）"""
    print("请使用 'uvicorn main:app --reload' 启动服务器")


if __name__ == "__main__":
    main()
