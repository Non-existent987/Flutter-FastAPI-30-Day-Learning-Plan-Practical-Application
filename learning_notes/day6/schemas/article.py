from sqlmodel import SQLModel  # 从sqlmodel导入SQLModel基类
from typing import Optional  # 导入Optional类型提示
from datetime import datetime  # 导入datetime时间处理模块

class ArticleBase(SQLModel):  # 定义ArticleBase基础模型类，继承SQLModel
    title: str  # 文章标题字段，字符串类型
    content: str  # 文章内容字段，字符串类型
    author: Optional[str] = None  # 文章作者字段，可选字符串类型，默认为空
    published: bool = False  # 发布状态字段，布尔类型，默认为False

class ArticleCreate(ArticleBase):  # 定义ArticleCreate创建模型类，继承ArticleBase
    pass  # 无额外字段，直接继承ArticleBase的所有字段

class ArticleUpdate(ArticleBase):  # 定义ArticleUpdate更新模型类，继承ArticleBase
    title: Optional[str] = None  # 可选的文章标题字段，默认为空
    content: Optional[str] = None  # 可选的文章内容字段，默认为空

class ArticleRead(ArticleBase):  # 定义ArticleRead读取模型类，继承ArticleBase
    id: int  # 文章ID字段，整数类型
    created_at: Optional[datetime] = None  # 创建时间字段，可选datetime类型，默认为空