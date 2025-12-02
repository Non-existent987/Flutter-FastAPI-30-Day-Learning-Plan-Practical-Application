# 导入所有模型以确保它们被注册到SQLModel.metadata中
from .article import Article
# from .user import User

__all__ = ["Article"]