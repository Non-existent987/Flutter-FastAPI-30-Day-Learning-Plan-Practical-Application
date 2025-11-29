# Day 3 详细学习计划：数据库集成(SQLite + SQLModel)

## 学习目标
- 学习 SQLModel 的基本用法
- 理解 ORM(Object Relational Mapping) 的概念
- 创建 SQLite 数据库并定义表结构
- 实现数据的增删改查操作

## 知识点详解

### 1. SQLModel 简介
**重要性：**
- 由 FastAPI 作者开发的库
- 结合了 SQLAlchemy 和 Pydantic 的优点
- 提供数据库模型和数据验证的统一接口

**安装命令：**
```bash
pip install sqlmodel
```

**特点：**
- 一次定义，既可用于数据库模型又可用于 Pydantic 模型
- 类型提示友好
- 自动生成表结构

### 2. SQLite 简介
**优势：**
- 轻量级文件型数据库
- 无需单独的服务器进程
- 零配置，无需额外安装
- 适合小型项目和原型开发

### 3. ORM 概念
**ORM (Object Relational Mapping)：**
- 对象关系映射
- 将数据库中的表映射为程序中的对象
- 通过操作对象来操作数据库

## 练习代码

### database.py
```python
from sqlmodel import SQLModel, create_engine, Field, Session
from typing import Optional
from datetime import datetime

# 定义文章模型，既是数据库模型又是 Pydantic 模型
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
engine = create_engine(DATABASE_URL, echo=True)

# 创建所有表
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# 获取数据库会话
def get_session():
    with Session(engine) as session:
        yield session
```

### main.py (更新版)
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from database import engine, Article, create_db_and_tables, get_session

app = FastAPI()

# 应用启动时创建数据库表
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# 创建文章
@app.post("/articles/", response_model=Article)
def create_article(article: Article, session: Session = Depends(get_session)):
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
        setattr(article, key, value)
    
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
```

## 易错点及解决方案

### 1. 数据库表未创建
**错误表现：**
```
no such table: article
```

**解决方案：**
确保在应用启动时调用了 `create_db_and_tables()` 函数

### 2. 循环导入问题
**错误场景：**
在多个文件间互相导入时出现循环导入

**解决方案：**
合理组织代码结构，将模型定义放在单独文件中

### 3. Session 使用不当
**错误示例：**
```python
session = Session(engine)
# 忘记关闭 session
```

**正确做法：**
```python
with Session(engine) as session:
    # 使用 session
    session.commit()
# session 自动关闭
```

### 4. 主键处理错误
**错误示例：**
```python
class Article(SQLModel, table=True):
    id: int  # 没有设置主键和默认值
```

**正确做法：**
```python
class Article(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
```

## 今日任务检查清单
- [ ] 理解 SQLModel 的作用和基本用法
- [ ] 创建 SQLite 数据库并定义 Article 表
- [ ] 实现文章的增删改查(CRUD)操作
- [ ] 测试数据库操作功能
- [ ] 理解 ORM 的基本概念

## 扩展阅读
- [SQLModel 官方文档](https://sqlmodel.tiangolo.com/)
- [SQLite 官方文档](https://www.sqlite.org/docs.html)
- [ORM 概念介绍](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping)