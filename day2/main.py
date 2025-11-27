from fastapi import FastAPI
from pydantic import BaseModel #导入pydantic 的基类
from typing import Optional

app = FastAPI()

# 定义数据模型
# 这个类，定义了前端必须发给你的数据格式
class Article(BaseModel):
    id : int = None
    title : str =  None
    content : str
    # 可选 ： 如果要自定义可选字段，可以使用 Optional[str] = None
    author : Optional[str] = None

# 创建一个接口使用这个模型
@app.post("/articles/")  
async def create_article(article: Article):

    # 这里的article参数已经是验证过的article对象了
    # 可以直接使用article.title, article.content

    # 模拟：我们只是把接收到的数据原样返回，证明解析成功
    return {
        "message" : "文章接收成功",
        "data" : article
    }