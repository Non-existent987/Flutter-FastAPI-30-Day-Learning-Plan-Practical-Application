from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select, Session
from typing import List
from markdown import markdown
from database import create_db_and_tables, get_session, engine
from schemas import ArticleCreate, ArticleRead, ArticleUpdate, Article
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时创建数据库表
    create_db_and_tables()
    yield
    # 应用关闭时可以执行清理工作

app = FastAPI(lifespan=lifespan,title="Tutorial Site API", version="0.1.0")

# 添加cors中间件，允许所有来源访问API，方法和头部
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],# 在生产环境中应指定允许的来源
    allow_credentials=True,# 允许cookie
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# 获取单个文章接口
@app.get("/articles/{article_id}", response_model=ArticleRead)
def read_article(*, article_id: int, session: Session = Depends(get_session)):
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return article

# 获取文章 html 内容接口
# @app.get("/articles/{article_id}/html", response_model=dict)
@app.get("/articles/{article_id}/html", response_class=HTMLResponse)
def read_article_html(*, article_id: int, session: Session = Depends(get_session)):
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    # 使用 markdown 库将 markdown 内容转换为 html
    print('======================',article.content,'=============================')
    html_content = markdown(article.content)
    # return {"id": article.id, "title": article.title, "html": html_content}
    return HTMLResponse(content=html_content)       
# 更新文章接口
@app.put("/articles/{article_id}", response_model=ArticleRead)
def update_article(*,
                   article_id: int,
                   article_update: ArticleUpdate,
                   session: Session = Depends(get_session)):
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    # 只更新提供的字段
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
                    session: Session = Depends(get_session),
                    article_id: int):
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    session.delete(article)
    session.commit()
    return {"ok": True}

# 根目录欢迎信息
@app.get("/")
def read_root():
    return {"message": "Welcome to the tutorial site API!"}
