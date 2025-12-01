from sqlmodel import SQLModel, Field
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