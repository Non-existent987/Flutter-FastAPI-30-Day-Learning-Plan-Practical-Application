# Day 7 详细学习计划：内容导入脚本开发

## 学习目标
- 创建批量内容导入脚本
- 学习自动化内容管理
- 完善后端功能

## 知识点详解

### 1. 批量内容导入
**用途：**
- 快速填充测试数据
- 导入已有内容
- 自动化部署的一部分

### 2. JSON 数据处理
**重要性：**
- 常见的数据交换格式
- 易于阅读和编辑
- 支持复杂数据结构

### 3. 自动化脚本开发
**好处：**
- 提高工作效率
- 减少重复劳动
- 降低人为错误

## 练习代码

### 内容导入脚本 import_content.py

```python
import json
from typing import List
from sqlmodel import Session
from database import engine, create_db_and_tables
from models.article import Article
from datetime import datetime

# 示例内容数据
sample_articles = [
    {
        "title": "Day 1: 环境搭建与 Hello World",
        "content": """# Day 1 学习内容

## 学习目标
- 安装 Python 3.10+ 和 VS Code
- 安装 FastAPI 和 uvicorn 库
- 创建第一个 FastAPI 应用并运行

## 知识点详解

### Python 环境安装
确保选择添加到系统 PATH 环境变量。

### FastAPI 和 uvicorn 安装
```bash
pip install fastapi uvicorn
```

### 第一个 FastAPI 应用
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

### 运行应用
```bash
uvicorn main:app --reload
```

## 总结
今天我们成功搭建了开发环境，并运行了第一个 FastAPI 应用。
""",
        "author": "教程作者",
        "published": True
    },
    {
        "title": "Day 2: 数据模型定义",
        "content": """# Day 2 学习内容

## 学习目标
- 学习 Pydantic 的基本用法
- 理解数据验证的重要性
- 定义 Article 数据模型

## 知识点详解

### Pydantic 简介
Pydantic 是一个数据验证和设置管理的库。

### 类型提示
Python 3.5+ 引入的功能，提高代码可读性和可维护性。

### 模型定义
```python
from pydantic import BaseModel
from typing import Optional

class Article(BaseModel):
    id: int
    title: str
    content: str
    author: Optional[str] = None
    published: bool = False
```

## 总结
今天我们学习了如何定义数据模型，并理解了类型提示的重要性。
""",
        "author": "教程作者",
        "published": True
    }
]

def import_sample_articles():
    """导入示例文章"""
    create_db_and_tables()
    
    with Session(engine) as session:
        for article_data in sample_articles:
            # 添加创建时间
            article_data['created_at'] = datetime.now()
            
            # 创建文章对象
            article = Article(**article_data)
            
            # 添加到数据库
            session.add(article)
        
        # 提交更改
        session.commit()
        print(f"成功导入 {len(sample_articles)} 篇文章")

if __name__ == "__main__":
    import_sample_articles()
```

### 从 JSON 文件导入内容

#### content.json
```json
[
  {
    "title": "Day 1: 环境搭建与 Hello World",
    "content": "# 第一天学习内容\n\n今天我们学习了...",
    "author": "作者名",
    "published": true
  },
  {
    "title": "Day 2: 数据模型定义",
    "content": "# 第二天学习内容\n\n今天我们学习了...",
    "author": "作者名",
    "published": true
  }
]
```

#### import_from_json.py
```python
import json
from datetime import datetime
from sqlmodel import Session
from database import engine, create_db_and_tables
from models.article import Article

def import_articles_from_json(json_file_path: str):
    """从 JSON 文件导入文章"""
    # 创建数据库表
    create_db_and_tables()
    
    # 读取 JSON 文件
    with open(json_file_path, 'r', encoding='utf-8') as f:
        articles_data = json.load(f)
    
    # 导入文章
    with Session(engine) as session:
        imported_count = 0
        for article_data in articles_data:
            # 添加创建时间
            article_data['created_at'] = datetime.now()
            
            # 创建文章对象
            article = Article(**article_data)
            
            # 添加到数据库
            session.add(article)
            imported_count += 1
        
        # 提交更改
        session.commit()
        print(f"成功从 {json_file_path} 导入 {imported_count} 篇文章")

if __name__ == "__main__":
    import_articles_from_json('content.json')
```

### 更高级的导入脚本 advanced_import.py

```python
import json
import argparse
from datetime import datetime
from sqlmodel import Session
from database import engine, create_db_and_tables
from models.article import Article

def import_articles(file_path: str, clear_existing: bool = False):
    """导入文章的通用函数"""
    # 创建数据库表
    create_db_and_tables()
    
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        if file_path.endswith('.json'):
            articles_data = json.load(f)
        else:
            # 如果不是 JSON 文件，尝试按行读取
            articles_data = []
            for line in f:
                articles_data.append(json.loads(line.strip()))
    
    # 导入文章
    with Session(engine) as session:
        # 如果需要清除现有数据
        if clear_existing:
            # 删除所有现有文章
            articles = session.exec("SELECT * FROM article").all()
            for article in articles:
                session.delete(article)
            session.commit()
            print("已清除现有文章")
        
        imported_count = 0
        for article_data in articles_data:
            # 添加创建时间
            if 'created_at' not in article_data:
                article_data['created_at'] = datetime.now()
            
            # 创建文章对象
            article = Article(**article_data)
            
            # 添加到数据库
            session.add(article)
            imported_count += 1
        
        # 提交更改
        session.commit()
        print(f"成功导入 {imported_count} 篇文章")

def main():
    parser = argparse.ArgumentParser(description='导入文章到数据库')
    parser.add_argument('file', help='要导入的文件路径')
    parser.add_argument('--clear', action='store_true', help='导入前清除现有数据')
    
    args = parser.parse_args()
    
    import_articles(args.file, args.clear)

if __name__ == "__main__":
    main()
```

## 易错点及解决方案

### 1. 文件编码问题
**问题：**
中文内容出现乱码

**解决方案：**
确保以 UTF-8 编码读取文件：
```python
with open(json_file_path, 'r', encoding='utf-8') as f:
    articles_data = json.load(f)
```

### 2. 数据格式不匹配
**问题：**
JSON 数据字段与模型字段不匹配

**解决方案：**
在导入前验证数据格式，或添加数据清洗逻辑

### 3. 重复导入问题
**问题：**
多次运行脚本导致数据重复

**解决方案：**
添加唯一性检查或提供清除选项

### 4. 时间格式处理
**问题：**
JSON 中的时间格式与 Python datetime 不兼容

**解决方案：**
添加时间格式转换逻辑：
```python
from datetime import datetime

# 如果 JSON 中是字符串时间
date_str = article_data.get('created_at')
if date_str:
    article_data['created_at'] = datetime.fromisoformat(date_str)
```

## 今日任务检查清单
- [ ] 创建内容导入脚本
- [ ] 导入前几天的学习内容
- [ ] 测试导入功能
- [ ] 完善后端功能

## 扩展阅读
- [JSON 处理](https://docs.python.org/3/library/json.html)
- [argparse 命令行参数处理](https://docs.python.org/3/library/argparse.html)
- [Python 文件 I/O](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)