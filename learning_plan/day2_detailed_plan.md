# Day 2 详细学习计划：数据模型定义

## 学习目标
- 学习 Pydantic 的基本用法
- 理解数据验证的重要性
- 定义 Article 数据模型
- 掌握类型提示 (Type Hints) 的使用

## 知识点详解

### 1. Pydantic 简介
**重要性：**
- 数据验证和设置管理的库
- FastAPI 内部使用 Pydantic 进行数据验证
- 提供类型提示和自动文档生成

**安装命令：**
```bash
pip install pydantic
```

### 2. 类型提示 (Type Hints)
**注意点：**
- Python 3.5+ 引入的功能
- 提高代码可读性和可维护性
- 帮助 IDE 提供更好的代码补全

**常用类型：**
- `str`: 字符串
- `int`: 整数
- `float`: 浮点数
- `bool`: 布尔值
- `Optional[T]`: 可选类型，等价于 `Union[T, None]`

### 3. Pydantic 模型定义
**关键概念：**
- 继承 BaseModel 类
- 字段类型声明
- 默认值设置
- 数据验证

## 练习代码

### models.py
```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 定义基础文章模型
class Article(BaseModel):
    id: int
    title: str
    content: str
    # 可选字段，可以为 None
    author: Optional[str] = None
    # 带默认值的字段
    published: bool = False
    # 时间戳字段
    created_at: Optional[datetime] = None

# 用于创建文章的模型
class ArticleCreate(BaseModel):
    title: str
    content: str
    author: Optional[str] = None

# 用于更新文章的模型
class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    published: Optional[bool] = None
```

### 使用示例 main.py
```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI()

class Article(BaseModel):
    id: int
    title: str
    content: str
    author: Optional[str] = None
    published: bool = False
    created_at: Optional[datetime] = None

# 存储文章的列表（临时用，后续会替换为数据库）
articles = []

@app.get("/")
def read_root():
    return {"Hello": "World"}

# 创建文章的接口
@app.post("/articles/")
def create_article(article: Article):
    articles.append(article)
    return article

# 获取所有文章的接口
@app.get("/articles/")
def read_articles():
    return articles
```

## 易错点及解决方案

### 1. 循环导入问题
**错误场景：**
在多个文件之间相互导入时可能出现循环导入

**解决方案：**
使用延迟导入或将共享模型放在单独的文件中

### 2. 类型注解错误
**错误示例：**
```python
class Article(BaseModel):
    id: int = "abc"  # 类型不匹配
```

**正确做法：**
```python
class Article(BaseModel):
    id: int = 1  # 或者不设置默认值，在创建实例时传入
```

### 3. 可选字段处理不当
**错误示例：**
```python
from typing import Optional

class Article(BaseModel):
    title: Optional[str]  # 没有默认值，创建实例时必须传入 None 或字符串
```

**推荐做法：**
```python
from typing import Optional

class Article(BaseModel):
    title: Optional[str] = None  # 设置默认值
```

## 今日任务检查清单
- [ ] 理解 Pydantic 的作用和基本用法
- [ ] 掌握 Python 类型提示的基本语法
- [ ] 定义 Article 数据模型及其相关操作模型
- [ ] 实现创建和获取文章的 API 接口
- [ ] 测试数据验证功能

## 扩展阅读
- [Pydantic 官方文档](https://pydantic-docs.helpmanual.io/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [FastAPI Data Models](https://fastapi.tiangolo.com/tutorial/body/)