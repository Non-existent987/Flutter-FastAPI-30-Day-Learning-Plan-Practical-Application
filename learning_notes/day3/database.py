from sqlmodel import SQLModel, create_engine, Field, Session
from typing import Optional
from datetime import datetime
from sqlmodel import Field
from typing import Optional, Union

# 定义文章模型，既是数据库模型又是pydantic的数据模型
class Article(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    author: Optional[str] = None
    published: bool = False
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_type=None)

# 数据库文件Url
DATABASE_URL = "sqlite:///./articles.db"

# 创建数据库引擎
engine = create_engine(DATABASE_URL, echo=True)

# 创建表格
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# 获取数据库会话
def get_session():
    with Session(engine) as session:
        yield session