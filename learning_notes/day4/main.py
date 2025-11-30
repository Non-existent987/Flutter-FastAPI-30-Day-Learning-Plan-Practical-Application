from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from database import create_db_and_tables, get_session
from schemas import Article, ArticleCreate, ArticleUpdate, ArticleRead
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时创建数据库表
    create_db_and_tables()
    yield
    # 应用关闭时可以执行清理工作

app = FastAPI(title="Tutorial Site API", version="0.1.0", lifespan=lifespan)


# 创建文章接口
@app.post("/articles/", response_model=ArticleRead, status_code=status.HTTP_201_CREATED)
def create_article(*,
                   article: ArticleCreate, 
                   session: Session = Depends(get_session)):
    db_article = Article.from_orm(article)
    session.add(db_article)
    session.commit()
    session.refresh(db_article)
    return db_article

# 获取所有文章接口
@app.get("/articles/", response_model=List[ArticleRead])
def read_articles(*, session: Session = Depends(get_session)):
    articles = session.exec(select(Article)).all()
    return articles

# 根据ID获取单个文章接口
@app.get("/articles/{article_id}", response_model=ArticleRead)
def read_article(*, article_id: int, session: Session = Depends(get_session)):
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

# 更新文章接口
@app.put("/articles/{article_id}", response_model=ArticleRead)
def update_article(*,
                   article_id: int,
                   article_update: ArticleUpdate,
                   session: Session = Depends(get_session)):
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    # 只更新提供了的字段
    article_data = article_update.dict(exclude_unset=True)
    for key, value in article_data.items():
        setattr(article, key, value)
    
    session.add(article)
    session.commit()
    session.refresh(article)
    return article
# 删除文章接口
@app.delete("/articles/{article_id}")
def delete_article(*,
                   article_id: int,
                   session: Session = Depends(get_session)):
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    session.delete(article)
    session.commit()
    return {"ok": True}

# 根目录欢迎信息
@app.get("/")
def read_root():
    return {"message": "Welcome to the tutorial site API!"}
