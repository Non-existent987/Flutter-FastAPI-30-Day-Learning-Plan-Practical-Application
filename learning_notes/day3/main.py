from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from contextlib import asynccontextmanager
from datetime import datetime
from database import engine, Article, create_db_and_tables, get_session

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时创建数据库表
    create_db_and_tables()
    yield
    # 应用关闭时可以执行清理工作

app = FastAPI(lifespan=lifespan)

# 创建文章
@app.post("/articles/", response_model=Article)
def create_article(article: Article, session: Session = Depends(get_session)):
    # 如果没有提供created_at，则使用当前时间
    if article.created_at is None:
        article.created_at = datetime.utcnow()
    session.add(article)
    session.commit()
    session.refresh(article)
    return article

# 获取所有文章
@app.get("/articles/", response_model=List[Article])
def read_articles(session: Session = Depends(get_session)):
    articles = session.exec(select(Article)).all()
    return articles

# 根据ID获取单个文章
@app.get("/articles/{article_id}", response_model=Article)
def read_article(article_id: int, session: Session = Depends(get_session)):
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

# 更新文章
@app.put("/articles/{article_id}", response_model=Article)
def update_article(
    article_id: int, 
    article_update: Article, 
    session: Session = Depends(get_session)
):
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # 更新文章字段
    article_data = article_update.dict(exclude_unset=True)
    for key, value in article_data.items():
        # 特殊处理created_at字段
        if key == "created_at" and isinstance(value, str):
            try:
                # 尝试解析ISO格式的日期字符串
                article_data[key] = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                # 如果解析失败，使用当前时间
                article_data[key] = datetime.utcnow()
        setattr(article, key, article_data[key])
    
    session.add(article)
    session.commit()
    session.refresh(article)
    return article

# 删除文章
@app.delete("/articles/{article_id}")
def delete_article(article_id: int, session: Session = Depends(get_session)):
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    session.delete(article)
    session.commit()
    return {"ok": True}