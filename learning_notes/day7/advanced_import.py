import argparse
from datetime import datetime
from sqlmodel import Session
from database import engine, create_db_and_tables
from models.article import Article

def import_articles(file_path: str, clear_existing: bool = False):
    """导入文章的通用函数"""
    # 创建数据库表
    create_db_and_tables()
    
    # 读取Markdown文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析Markdown文件获取标题
    lines = content.split('\n')
    title = "默认标题"
    for line in lines:
        if line.startswith('# '):
            title = line[2:]  # 移除 "# " 前缀
            break
    
    # 使用文件名（不含扩展名）作为备选标题
    if title == "默认标题":
        import os
        title = os.path.splitext(os.path.basename(file_path))[0]
    
    # 导入文章
    with Session(engine) as session:
        # 如果需要清除现有数据
        if clear_existing:
            # 删除所有现有文章
            articles = session.query(Article).all()
            for article in articles:
                session.delete(article)
            session.commit()
            print("已清除现有文章")
        
        # 创建新文章对象
        article = Article(
            title=title,
            content=content,
            created_at=datetime.now()
        )
        
        # 添加到数据库
        session.add(article)
        session.commit()
        session.refresh(article)
        print(f"成功导入文章: {article.title}")

def main():
    parser = argparse.ArgumentParser(description='导入文章到数据库')
    parser.add_argument('file', help='要导入的Markdown文件路径')
    parser.add_argument('--clear', action='store_true', help='导入前清除现有数据')
    
    args = parser.parse_args()
    
    import_articles(args.file, args.clear)

if __name__ == "__main__":
    # 为了测试方便，可以暂时使用固定路径
    import_articles('./第七天的内容.md', True)
    # main()  # 正常情况下使用命令行参数