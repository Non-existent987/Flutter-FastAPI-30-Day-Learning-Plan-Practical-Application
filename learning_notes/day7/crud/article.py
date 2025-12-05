from sqlmodel import Session, select  # 从sqlmodel导入Session会话和select查询函数
from models.article import Article  # 从models.article导入Article数据模型
from schemas.article import ArticleCreate, ArticleUpdate  # 从schemas.article导入ArticleCreate和ArticleUpdate模型
from typing import List, Optional  # 导入List和Optional类型提示

def create_article(session: Session, article_create: ArticleCreate) -> Article:  # 定义创建文章函数，接收会话和创建文章参数，返回Article对象
    # 下面的.from_orm方法被弃用了怎么办？
    # db_article = Article.from_orm(article_create)  # 从ORM对象创建Article实例
    db_article = Article(**article_create.model_dump())
    session.add(db_article)  # 将文章对象添加到会话中
    session.commit()  # 提交会话，保存更改到数据库
    session.refresh(db_article)  # 刷新文章对象，获取数据库中的最新数据
    return db_article  # 返回创建的文章对象

def get_articles(session: Session) -> List[Article]:  # 定义获取所有文章函数，接收会话参数，返回Article列表
    articles = session.exec(select(Article)).all()  # 执行查询获取所有文章
    return articles  # 返回文章列表

def get_article_by_id(session: Session, article_id: int) -> Optional[Article]:  # 定义根据ID获取文章函数，接收会话和文章ID参数，返回可选的Article对象
    article = session.get(Article, article_id)  # 根据ID获取文章
    return article  # 返回文章对象或None

def update_article(session: Session, article_id: int, article_update: ArticleUpdate) -> Optional[Article]:  # 定义更新文章函数，接收会话、文章ID和更新参数，返回可选的Article对象
    article = session.get(Article, article_id)  # 根据ID获取文章
    if not article:  # 如果文章不存在
        return None  # 返回None
    
    article_data = article_update.dict(exclude_unset=True)  # 将更新参数转换为字典，排除未设置的字段
    for key, value in article_data.items():  # 遍历更新数据
        setattr(article, key, value)  # 设置文章对象的属性值
    
    session.add(article)  # 将更新后的文章对象添加到会话中
    session.commit()  # 提交会话，保存更改到数据库
    session.refresh(article)  # 刷新文章对象，获取数据库中的最新数据
    return article  # 返回更新后的文章对象

def delete_article(session: Session, article_id: int) -> bool:  # 定义删除文章函数，接收会话和文章ID参数，返回布尔值
    article = session.get(Article, article_id)  # 根据ID获取文章
    if not article:  # 如果文章不存在
        return False  # 返回False
    
    session.delete(article)  # 从会话中删除文章对象
    session.commit()  # 提交会话，保存更改到数据库
    return True  # 返回True表示删除成功