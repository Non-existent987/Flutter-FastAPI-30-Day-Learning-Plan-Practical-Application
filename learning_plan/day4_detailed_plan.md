# Day 4 详细学习计划：完整 CRUD 操作实现

## 学习目标
- 理解 RESTful API 设计原则
- 实现完整的增删改查接口
- 学习 FastAPI 的依赖注入系统
- 掌握数据库会话(Session)管理

## 知识点详解

### 1. RESTful API 设计原则
**核心概念：**
- 使用标准 HTTP 方法：GET(查询)、POST(创建)、PUT(更新)、DELETE(删除)
- URI 表示资源：/articles 表示文章集合，/articles/1 表示特定文章
- 无状态：每次请求应包含所有必要信息

**常见的 HTTP 状态码：**
- 200 OK：请求成功
- 201 Created：创建成功
- 400 Bad Request：客户端请求错误
- 404 Not Found：资源不存在
- 500 Internal Server Error：服务器内部错误

### 2. FastAPI 依赖注入系统
**概念：**
- 自动处理依赖关系
- 减少重复代码
- 提高代码可测试性和可维护性

**常用场景：**
- 数据库会话管理
- 认证和授权
- 配置参数传递

### 3. 数据库会话管理
**重要性：**
- 管理与数据库的连接
- 控制事务边界
- 确保数据一致性

## 练习代码

### database.py (扩展)
```python
from sqlmodel import SQLModel, create_engine, Field, Session
from typing import Optional
from datetime import datetime

class Article(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    author: Optional[str] = None
    published: bool = False
    created_at: Optional[datetime] = None

# 数据库文件 URL
DATABASE_URL = "sqlite:///./tutorial.db"

# 创建数据库引擎
# echo=True 会在控制台输出 SQL 语句，便于调试
engine = create_engine(DATABASE_URL, echo=True)

# 创建所有表
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# 获取数据库会话
def get_session():
    with Session(engine) as session:
        yield session
```

### schemas.py (数据模型分离)
```python
from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime

# 数据库模型和响应模型共用的基础模型
class ArticleBase(SQLModel):
    title: str
    content: str
    author: Optional[str] = None
    published: bool = False

# 数据库模型
class Article(ArticleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = None

# 创建文章时使用的模型
class ArticleCreate(ArticleBase):
    pass

# 更新文章时使用的模型
class ArticleUpdate(ArticleBase):
    title: Optional[str] = None
    content: Optional[str] = None

# 数据库返回的文章模型
class ArticleRead(ArticleBase):
    id: int
    created_at: Optional[datetime] = None
```

### main.py (完整 CRUD 版)
```python
from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from database import engine, create_db_and_tables, get_session
from schemas import Article, ArticleCreate, ArticleRead, ArticleUpdate

app = FastAPI(title="Tutorial Site API", version="0.1.0")

# 应用启动时创建数据库表
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# 创建文章接口
@app.post("/articles/", response_model=ArticleRead, status_code=status.HTTP_201_CREATED)
def create_article(*, session: Session = Depends(get_session), article: ArticleCreate):
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
def read_article(*, session: Session = Depends(get_session), article_id: int):
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

# 更新文章接口
@app.put("/articles/{article_id}", response_model=ArticleRead)
def update_article(
    *, 
    session: Session = Depends(get_session), 
    article_id: int, 
    article_update: ArticleUpdate
):
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
def delete_article(*, session: Session = Depends(get_session), article_id: int):
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    session.delete(article)
    session.commit()
    return {"ok": True}

# 根目录欢迎信息
@app.get("/")
def read_root():
    return {"message": "Welcome to Tutorial Site API"}
```

## 易错点及解决方案

### 1. 依赖注入使用错误
**错误示例：**
```python
# 错误：没有使用 Depends
def create_article(session: Session, article: ArticleCreate):
    pass
```

**正确做法：**
```python
# 正确：使用 Depends 注入依赖
def create_article(*, session: Session = Depends(get_session), article: ArticleCreate):
    pass
```

### 2. 模型转换问题
**错误示例：**
```python
# 忘记配置 orm_mode
class ArticleRead(ArticleBase):
    id: int
    
# 在转换时出错
db_article = Article.from_orm(article_create)
```

**解决方案：**
确保在需要 ORM 转换的模型中启用 orm_mode（SQLModel 默认支持）

### 3. 状态码设置不当
**改进点：**
为不同操作设置合适的 HTTP 状态码，提高 API 的专业性

### 4. 异常处理不完善
**增强点：**
为各种异常情况提供清晰的错误信息和合适的 HTTP 状态码

## 今日任务检查清单
- [ ] 理解 RESTful API 设计原则
- [ ] 实现文章的完整 CRUD 操作
- [ ] 学习并使用 FastAPI 的依赖注入系统
- [ ] 分离数据模型，提高代码可维护性
- [ ] 设置正确的 HTTP 状态码
- [ ] 添加完善的异常处理

## 扩展阅读
- [RESTful API 设计指南](https://restfulapi.net/)
- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)