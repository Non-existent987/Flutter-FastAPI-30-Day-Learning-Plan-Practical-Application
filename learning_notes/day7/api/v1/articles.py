from fastapi import APIRouter, Depends, HTTPException, status  # 从fastapi导入所需模块
from sqlmodel import Session  # 从sqlmodel导入Session会话
from typing import List  # 导入List类型提示
from database import get_session  # 从database模块导入get_session函数
from crud.article import create_article, get_articles, get_article_by_id, update_article, delete_article  # 从crud.article导入各种操作函数
from schemas.article import ArticleCreate, ArticleRead, ArticleUpdate  # 从schemas.article导入各种模型

router = APIRouter(prefix="/articles", tags=["articles"])  # 创建API路由器，设置路由前缀和标签

@router.post("/", response_model=ArticleRead, status_code=status.HTTP_201_CREATED)  # 定义创建文章的POST路由，设置响应模型和状态码
def create_new_article(*, session: Session = Depends(get_session), article: ArticleCreate):  # 定义创建新文章的处理函数
    return create_article(session, article)  # 调用crud模块的create_article函数创建文章

@router.get("/", response_model=List[ArticleRead])  # 定义获取所有文章的GET路由，设置响应模型为文章列表
def read_all_articles(*, session: Session = Depends(get_session)):  # 定义获取所有文章的处理函数
    return get_articles(session)  # 调用crud模块的get_articles函数获取所有文章

@router.get("/{article_id}", response_model=ArticleRead)  # 定义获取单个文章的GET路由，设置响应模型
def read_single_article(*, session: Session = Depends(get_session), article_id: int):  # 定义获取单个文章的处理函数
    article = get_article_by_id(session, article_id)  # 调用crud模块的get_article_by_id函数获取文章
    if not article:  # 如果文章不存在
        raise HTTPException(status_code=404, detail="Article not found")  # 抛出404异常
    return article  # 返回文章对象

@router.put("/{article_id}", response_model=ArticleRead)  # 定义更新文章的PUT路由，设置响应模型
def update_single_article(  # 定义更新文章的处理函数
    *,  # 强制关键字参数
    session: Session = Depends(get_session),  # 数据库会话依赖
    article_id: int,  # 文章ID参数
    article_update: ArticleUpdate  # 文章更新数据
):
    article = update_article(session, article_id, article_update)  # 调用crud模块的update_article函数更新文章
    if not article:  # 如果文章不存在
        raise HTTPException(status_code=404, detail="Article not found")  # 抛出404异常
    return article  # 返回更新后的文章对象

@router.delete("/{article_id}")  # 定义删除文章的DELETE路由
def delete_single_article(*, session: Session = Depends(get_session), article_id: int):  # 定义删除文章的处理函数
    success = delete_article(session, article_id)  # 调用crud模块的delete_article函数删除文章
    if not success:  # 如果删除失败
        raise HTTPException(status_code=404, detail="Article not found")  # 抛出404异常
    return {"ok": True}  # 返回删除成功的信息