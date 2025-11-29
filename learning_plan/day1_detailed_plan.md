# Day 1 详细学习计划：环境搭建与 Hello World

## 学习目标
- 安装 Python 3.10+ 和 VS Code
- 安装 FastAPI 和 uvicorn 库
- 创建第一个 FastAPI 应用并运行
- 理解基本的 REST API 概念

## 知识点详解

### 1. Python 环境安装与配置
**注意点：**
- 确保选择添加到系统 PATH 环境变量
- 推荐使用 Python 3.10 或更高版本
- 可考虑使用虚拟环境隔离项目依赖

**验证命令：**
```bash
python --version
pip --version
```

### 2. FastAPI 和 uvicorn 安装
**注意点：**
- FastAPI 是一个现代、快速(高性能)的 Web 框架
- Uvicorn 是一个 ASGI 服务器，用于运行 FastAPI 应用

**安装命令：**
```bash
pip install fastapi uvicorn
```

### 3. 创建第一个 FastAPI 应用
**关键概念：**
- 路径操作装饰器 (@app.get)
- 路径操作函数
- 自动交互式 API 文档 (Swagger UI)

## 练习代码

### main.py
```python
from fastapi import FastAPI

# 创建 FastAPI 实例
app = FastAPI()

# 定义根路径的 GET 请求处理函数
@app.get("/")
def read_root():
    return {"Hello": "World"}

# 定义带参数的 GET 请求处理函数
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

### 运行应用
```bash
uvicorn main:app --reload
```

## 易错点及解决方案

### 1. 导入错误
**错误示例：**
```
ModuleNotFoundError: No module named 'fastapi'
```
**解决方案：**
确保已经正确安装了 fastapi 包

### 2. 端口占用
**错误示例：**
```
OSError: [Errno 98] Address already in use
```
**解决方案：**
更换端口号
```bash
uvicorn main:app --port 8001 --reload
```

### 3. 无法访问 API 文档
**可能原因：**
- 服务器未正常启动
- 浏览器访问地址错误
**解决方案：**
确认访问地址为 http://127.0.0.1:8000/docs

## 今日任务检查清单
- [ ] 安装 Python 3.10+ 和 VS Code
- [ ] 安装 FastAPI 和 uvicorn
- [ ] 创建 main.py 文件并编写第一个 FastAPI 应用
- [ ] 成功运行应用并在浏览器中访问
- [ ] 理解 @app.get 装饰器的作用
- [ ] 查看并理解自动生成的 API 文档

## 扩展阅读
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [ASGI 服务器介绍](https://asgi.readthedocs.io/en/latest/)
- [REST API 设计原则](https://restfulapi.net/)