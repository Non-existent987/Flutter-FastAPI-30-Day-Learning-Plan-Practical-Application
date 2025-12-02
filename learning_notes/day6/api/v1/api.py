from fastapi import APIRouter  # 从fastapi导入APIRouter
from api.v1.articles import router as articles_router  # 从api.v1.articles导入路由并重命名为articles_router

api_router = APIRouter()  # 创建主API路由器
api_router.include_router(articles_router)  # 将文章路由包含到主API路由器中