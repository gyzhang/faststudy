from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers import users, items
from config import settings
from models.database import init_db

# 初始化数据库
init_db()

# 创建 FastAPI 应用实例
app = FastAPI(
    title=settings.APP_NAME,
    description="FastAPI 学习项目 - 包含常用功能演示",
    version="1.0.0"
)

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 包含路由
app.include_router(users.router, prefix="/api/v1", tags=["用户管理"])
app.include_router(items.router, prefix="/api/v1", tags=["物品管理"])


@app.get("/", tags=["根路径"])
async def root():
    """欢迎页面 - 重定向到静态首页"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/static/index.html")


@app.get("/health", tags=["健康检查"])
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """返回网站图标"""
    return FileResponse("static/favicon.svg")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )