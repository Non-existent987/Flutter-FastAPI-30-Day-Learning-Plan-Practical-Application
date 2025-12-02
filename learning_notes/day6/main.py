from contextlib import asynccontextmanager
from fastapi import FastAPI  # 导入FastAPI框架
from fastapi.middleware.cors import CORSMiddleware  # 导入CORS中间件，用于处理跨域请求
from api.v1.api import api_router
from database import create_db_and_tables  # 导入API路由


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时创建数据库表
    create_db_and_tables()
    yield
    # 应用关闭时可以执行清理工作

app = FastAPI(title="Tutorial Site API", version="1.0.0", lifespan=lifespan)  # 创建FastAPI应用实例，设置标题和版本
# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,  # 使用CORS中间件
    allow_origins=["*"],  # 允许所有来源的跨域请求
    allow_credentials=True,  # 允许携带凭证信息
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)

# 包含 API 路由
app.include_router(api_router, prefix="/api/v1")  # 包含API路由，并设置路由前缀为/api/v1

@app.get("/")  # 定义根路径的GET请求处理函数
def read_root():  # 根路径处理函数
    return {"message": "Welcome to Tutorial Site API"}  # 返回欢迎信息

