from sqlmodel import SQLModel, Field  # 从sqlmodel导入SQLModel基类和Field字段定义
from typing import Optional  # 导入Optional类型提示
from datetime import datetime  # 导入datetime时间处理模块

class Article(SQLModel, table=True):  # 定义Article数据模型类，继承SQLModel并映射为数据库表,table=True表示映射为数据库表
    id: Optional[int] = Field(default=None, primary_key=True)  # 文章ID字段，主键，默认为空
    title: str  # 文章标题字段，字符串类型
    content: str  # 文章内容字段，字符串类型
    author: Optional[str] = None  # 文章作者字段，可选字符串类型，默认为空
    published: bool = False  # 发布状态字段，布尔类型，默认为False
    created_at: Optional[datetime] = None  # 创建时间字段，可选datetime类型，默认为空