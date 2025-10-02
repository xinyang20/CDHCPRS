"""
慢性病诊疗方案推荐系统 - FastAPI 应用入口
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import get_settings
from routers import admin, auth, chat, public


def create_app() -> FastAPI:
    """构建并返回 FastAPI 应用实例"""

    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        description="基于大语言模型的慢性病诊疗方案推荐系统",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 生产环境请配置具体域名
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router)
    app.include_router(public.router)
    app.include_router(chat.router)
    app.include_router(admin.router)

    return app


app = create_app()


@app.get("/")
def root():
    """根路径"""
    settings = get_settings()
    return {
        "message": f"欢迎使用{settings.APP_NAME} API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/api/health")
def health_check():
    """健康检查接口"""
    settings = get_settings()
    return {
        "status": "healthy",
        "message": f"{settings.APP_NAME} 后端服务运行正常",
        "version": "1.0.0",
    }


def main() -> None:
    """主函数（用于 uv 兼容提示）"""
    print("请使用 'uvicorn main:app --reload' 启动服务器")


if __name__ == "__main__":
    main()
