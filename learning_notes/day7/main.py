from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_db_and_tables
from api.v1.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时创建数据库表
    create_db_and_tables()
    yield
    # 应用关闭时可以执行清理工作


app = FastAPI(lifespan=lifespan, title="Tutorial Site API", version="1.0.0")  # 创建FastAPI应用实例，设置标题和版本

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的源
    allow_credentials=True,
    allow_methods=["*"],  # 允许的 HTTP 方法
    allow_headers=["*"],  # 允许的 HTTP 头
)
# 包含 API 路由
app.include_router(api_router, prefix="/api/v1")  # 包含API路由，并设置路由前缀为/api/v1

@app.get("/")  # 定义根路径的GET请求处理函数
def read_root():
    return {"message": "Welcome to Tutorial Site API"}  # 返回欢迎信息