# Day 5 详细学习计划：Markdown 支持与 CORS 配置

## 学习目标
- 为文章内容添加 Markdown 支持
- 配置 CORS 解决跨域问题
- 学习 API 测试方法
- 使用 Postman 或 Swagger UI 测试接口

## 知识点详解

### 1. Markdown 简介
**概念：**
- 轻量级标记语言
- 易于阅读和编写
- 可转换为有效的 XHTML 或 HTML 文档

**常用语法：**
- 标题：`# H1`, `## H2`, `### H3`
- 粗体：`**粗体文本**`
- 斜体：`*斜体文本*`
- 列表：`- 项目1` 或 `1. 项目1`
- 链接：`[链接文本](URL)`
- 图片：`![替代文本](图片URL)`
- 代码块：```` ```代码``` ````

### 2. CORS (Cross-Origin Resource Sharing)
**产生原因：**
- 浏览器同源策略限制
- 前端(localhost:3000)和后端(localhost:8000)端口不同构成跨域

**解决方法：**
- 后端配置允许跨域请求
- 使用 FastAPI 的 CORSMiddleware

### 3. API 测试工具
**Swagger UI：**
- FastAPI 自带
- 访问 `/docs` 查看
- 可在线测试接口

**Postman：**
- 功能强大的 API 测试工具
- 支持各种 HTTP 方法
- 可保存测试用例

## 练习代码

### main.py (添加 CORS 支持)
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware  # 导入 CORS 中间件
from sqlmodel import Session, select
from typing import List
import markdown  # 用于 Markdown 转换
from database import engine, create_db_and_tables, get_session
from schemas import Article, ArticleCreate, ArticleRead, ArticleUpdate

app = FastAPI(title="Tutorial Site API", version="0.1.0")

# 添加 CORS 中间件，允许所有来源、方法和头部
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# 根据ID获取单个文章接口（返回 HTML 格式内容）
@app.get("/articles/{article_id}", response_model=ArticleRead)
def read_article(*, session: Session = Depends(get_session), article_id: int):
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

# 获取文章 HTML 内容接口
@app.get("/articles/{article_id}/html")
def read_article_html(*, session: Session = Depends(get_session), article_id: int):
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # 将 Markdown 转换为 HTML
    html_content = markdown.markdown(article.content)
    return {"id": article.id, "title": article.title, "content": html_content}

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

### 安装 Markdown 支持
```bash
pip install markdown
```

### 示例 Markdown 文章内容
```markdown
# 我的第一个教程

## 简介

欢迎来到我的教程网站！在这里我们将一起学习如何使用 FastAPI 和 Flutter 构建一个完整的网站。

## 安装步骤

1. 安装 Python 3.10+
2. 安装必要的依赖包：
   ```
   pip install fastapi uvicorn sqlmodel
   ```
3. 创建项目目录

## 第一个 FastAPI 应用

创建 `main.py` 文件：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

运行应用：
```bash
uvicorn main:app --reload
```

## 总结

今天我们一起完成了：
- 环境搭建
- 第一个 FastAPI 应用
- API 测试

明天我们将继续学习数据模型的定义。
```

## 使用 Postman 测试 API

### 1. 创建文章
- 方法：POST
- URL：http://localhost:8000/articles/
- Body 类型：JSON
- 内容：
```json
{
  "title": "使用 Postman 测试 API",
  "content": "# Postman 教程\n\n## 简介\nPostman 是一个强大的 API 测试工具。\n\n## 使用步骤\n1. 打开 Postman\n2. 创建新请求\n3. 输入 URL 和方法\n4. 发送请求",
  "author": "你的名字"
}
```

### 2. 获取文章列表
- 方法：GET
- URL：http://localhost:8000/articles/

### 3. 获取单篇文章
- 方法：GET
- URL：http://localhost:8000/articles/1

### 4. 获取文章 HTML 内容
- 方法：GET
- URL：http://localhost:8000/articles/1/html

## 易错点及解决方案

### 1. CORS 配置错误
**问题：**
前端访问后端 API 时报错：
```
Access to fetch at 'http://localhost:8000/articles/' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

**解决方案：**
确保正确添加了 CORSMiddleware，并且配置允许对应的方法和头部。

### 2. Markdown 渲染问题
**问题：**
Markdown 内容没有正确转换为 HTML

**解决方案：**
确保安装了 markdown 库，并正确调用 `markdown.markdown()` 函数。

### 3. 生产环境 CORS 配置
**安全隐患：**
```python
allow_origins=["*"]  # 允许所有来源，存在安全风险
```

**生产环境推荐配置：**
```python
allow_origins=["https://yourdomain.com", "https://www.yourdomain.com"]
```

### 4. Markdown 扩展支持
**增强功能：**
可以通过安装扩展来支持更多 Markdown 语法：
```bash
pip install markdown[extra]
```

```python
import markdown

# 使用扩展
html_content = markdown.markdown(
    article.content, 
    extensions=['extra', 'codehilite']
)
```

## 今日任务检查清单
- [ ] 为后端 API 添加 CORS 支持
- [ ] 实现 Markdown 到 HTML 的转换
- [ ] 使用 Postman 测试所有 API 接口
- [ ] 通过 Swagger UI (/docs) 测试 API
- [ ] 创建几篇包含 Markdown 语法的测试文章

## 扩展阅读
- [FastAPI CORS 文档](https://fastapi.tiangolo.com/tutorial/cors/)
- [Markdown 语法说明](https://markdown.com.cn/)
- [Postman 官方文档](https://learning.postman.com/docs/getting-started/introduction/)