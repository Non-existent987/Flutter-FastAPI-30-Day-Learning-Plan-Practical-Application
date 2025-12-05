from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

# 定义数据库连接URL
DATABASE_URL = "sqlite:///./tutorial.db"

# 创建数据库引擎
engine = create_engine(DATABASE_URL, echo=True)


# 创建数据库表
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# 获取数据库会话
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

