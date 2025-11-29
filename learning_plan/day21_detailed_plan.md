# Day 21 详细学习计划：Docker 化后端服务

## 学习目标
- 学习 Docker 基础知识
- 创建 FastAPI 应用的 Dockerfile
- 构建并运行 Docker 镜像
- 理解容器化部署优势

## 知识点详解

### 1. Docker 基础概念
**核心概念：**
- 镜像(Image)：只读模板，包含运行应用所需的所有内容
- 容器(Container)：镜像的运行实例
- Dockerfile：构建镜像的指令文件
- 仓库(Registry)：存储和分发镜像的地方

**优势：**
- 环境一致性
- 快速部署
- 资源隔离
- 易于扩展

### 2. Dockerfile 编写
**基本指令：**
- FROM：指定基础镜像
- WORKDIR：设置工作目录
- COPY：复制文件到镜像
- RUN：执行命令
- EXPOSE：声明端口
- CMD/ENTRYPOINT：指定容器启动时执行的命令

### 3. 多阶段构建
**优势：**
- 减小镜像体积
- 提高构建效率
- 分离构建和运行环境

## 练习代码

### 1. 创建后端 Dockerfile

#### 在项目根目录创建 Dockerfile
```dockerfile
# 使用 Python 3.9 slim 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装系统依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libc-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制 requirements.txt 文件
COPY ./requirements.txt /app/requirements.txt

# 安装 Python 依赖
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . /app

# 暴露端口
EXPOSE 8000

# 创建非 root 用户
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# 启动应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. 创建 requirements.txt

#### 在项目根目录创建 requirements.txt
```txt
fastapi==0.95.0
uvicorn[standard]==0.21.1
sqlmodel==0.0.8
pydantic==1.10.7
markdown==3.4.3
```

### 3. 更新 FastAPI 应用以支持 Docker

#### 更新 main.py
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# 从环境变量获取主机地址，默认为 localhost
host = os.getenv("HOST", "127.0.0.1")
port = int(os.getenv("PORT", 8000))

app = FastAPI(
    title="Tutorial Site API",
    description="Flutter + FastAPI 30天速成网站后端API",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
# 注意：这里需要根据你的实际路由结构进行调整
from api.v1.api import api_router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Tutorial Site API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 应用启动时创建数据库表
from database import create_db_and_tables

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=host, port=port)
```

### 4. 创建 docker-compose.yml 文件

#### 在项目根目录创建 docker-compose.yml
```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./tutorial.db:/app/tutorial.db
      - ./logs:/app/logs
    environment:
      - HOST=0.0.0.0
      - PORT=8000
    restart: unless-stopped
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### 5. 创建 .dockerignore 文件

#### 在项目根目录创建 .dockerignore
```dockerignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# Logs
logs/
*.log

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Test files
tests/
test_*.py
```

### 6. 创建构建脚本

#### 创建 scripts/build_docker.sh (Linux/Mac)
```bash
#!/bin/bash

# 构建 Docker 镜像
echo "Building Docker image..."
docker build -t tutorial-site-backend:latest .

# 查看构建的镜像
echo "Listing Docker images..."
docker images | grep tutorial-site-backend

echo "Build completed!"
```

#### 创建 scripts/build_docker.bat (Windows)
```batch
@echo off

REM 构建 Docker 镜像
echo Building Docker image...
docker build -t tutorial-site-backend:latest .

REM 查看构建的镜像
echo Listing Docker images...
docker images | findstr tutorial-site-backend

echo Build completed!
```

### 7. 创建运行脚本

#### 创建 scripts/run_docker.sh (Linux/Mac)
```bash
#!/bin/bash

# 运行 Docker 容器
echo "Running Docker container..."
docker run -d \
  --name tutorial-backend \
  -p 8000:8000 \
  -v $(pwd)/tutorial.db:/app/tutorial.db \
  -v $(pwd)/logs:/app/logs \
  tutorial-site-backend:latest

# 查看运行的容器
echo "Checking running containers..."
docker ps | grep tutorial-backend

echo "Container is running at http://localhost:8000"
```

#### 创建 scripts/run_docker.bat (Windows)
```batch
@echo off

REM 运行 Docker 容器
echo Running Docker container...
docker run -d ^
  --name tutorial-backend ^
  -p 8000:8000 ^
  -v %cd%/tutorial.db:/app/tutorial.db ^
  -v %cd%/logs:/app/logs ^
  tutorial-site-backend:latest

REM 查看运行的容器
echo Checking running containers...
docker ps | findstr tutorial-backend

echo Container is running at http://localhost:8000
```

### 8. 创建开发环境脚本

#### 创建 scripts/dev_docker.sh (Linux/Mac)
```bash
#!/bin/bash

# 开发模式运行 Docker 容器（带热重载）
echo "Running Docker container in development mode..."
docker run -d \
  --name tutorial-backend-dev \
  -p 8000:8000 \
  -v $(pwd):/app \
  tutorial-site-backend:latest \
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 查看运行的容器
echo "Checking running containers..."
docker ps | grep tutorial-backend-dev

echo "Development container is running at http://localhost:8000"
```

### 9. 测试 Docker 部署

#### 创建测试脚本 scripts/test_docker.sh (Linux/Mac)
```bash
#!/bin/bash

echo "Testing Docker deployment..."

# 检查容器是否运行
if docker ps | grep -q tutorial-backend; then
    echo "Container is running"
else
    echo "Container is not running"
    exit 1
fi

# 测试健康检查端点
echo "Testing health endpoint..."
curl -f http://localhost:8000/health || {
    echo "Health check failed"
    exit 1
}

# 测试根端点
echo "Testing root endpoint..."
curl -f http://localhost:8000/ || {
    echo "Root endpoint test failed"
    exit 1
}

echo "All tests passed!"
```

## Docker 常用命令

### 构建镜像
```bash
docker build -t tutorial-site-backend:latest .
```

### 运行容器
```bash
docker run -d --name tutorial-backend -p 8000:8000 tutorial-site-backend:latest
```

### 查看运行中的容器
```bash
docker ps
```

### 查看容器日志
```bash
docker logs tutorial-backend
```

### 停止容器
```bash
docker stop tutorial-backend
```

### 删除容器
```bash
docker rm tutorial-backend
```

### 进入容器命令行
```bash
docker exec -it tutorial-backend /bin/bash
```

## 易错点及解决方案

### 1. 端口冲突
**问题：**
8000 端口已被占用

**解决方案：**
```bash
# 使用其他端口
docker run -d --name tutorial-backend -p 8001:8000 tutorial-site-backend:latest
```

### 2. 权限问题
**问题：**
无法访问数据库文件

**解决方案：**
确保数据库文件权限正确，或在 Dockerfile 中正确设置用户权限

### 3. 依赖安装失败
**问题：**
某些 Python 包安装失败

**解决方案：**
在 Dockerfile 中安装必要的系统依赖，如 gcc、libc-dev 等

### 4. 网络连接问题
**问题：**
容器无法访问外部网络

**解决方案：**
检查 Docker 网络配置，确保容器可以访问所需服务

## 今日任务检查清单
- [ ] 创建后端 Dockerfile
- [ ] 编写 requirements.txt
- [ ] 创建 docker-compose.yml 文件
- [ ] 构建 Docker 镜像
- [ ] 运行 Docker 容器
- [ ] 测试 API 是否正常工作

## 扩展阅读
- [Docker 官方文档](https://docs.docker.com/)
- [Dockerfile 最佳实践](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [FastAPI 部署指南](https://fastapi.tiangolo.com/deployment/)