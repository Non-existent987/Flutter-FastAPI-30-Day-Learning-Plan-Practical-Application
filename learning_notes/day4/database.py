from sqlmodel import SQLModel, create_engine, Field, Session
from typing import Optional
from datetime import datetime



# 数据库文件Url
DATABASE_URL = "sqlite:///./articles.db"

# 创建数据库引擎，echo=True表示打印SQL语句
engine = create_engine(DATABASE_URL, echo=True)

# 创建所有表
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# 获取数据库会话
def get_session():
    with Session(engine) as session:
        yield session #yield作用是返回一个迭代器，迭代器中的数据是yield后面的数据