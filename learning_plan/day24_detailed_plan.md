# Day 24 详细学习计划：服务器部署与配置

## 学习目标
- 学习服务器环境搭建
- 配置 Docker 和 Docker Compose
- 部署完整应用栈
- 验证部署结果

## 知识点详解

### 1. 服务器环境准备
**操作系统选择：**
- Ubuntu Server LTS（推荐）
- CentOS/RHEL
- Debian

**基础配置：**
- 用户权限管理
- 防火墙配置
- SSH 安全设置

### 2. Docker 环境安装
**安装步骤：**
- 安装 Docker Engine
- 安装 Docker Compose
- 配置 Docker 用户组

**验证安装：**
- Docker 版本检查
- Hello World 测试
- 权限验证

### 3. 应用部署流程
**部署步骤：**
- 代码传输
- 环境变量配置
- 服务启动
- 健康检查

## 练习代码

### 1. 创建服务器初始化脚本

#### 创建 scripts/server_setup.sh (Linux/Mac)
```bash
#!/bin/bash

# 服务器初始化脚本
echo "Initializing server setup..."

# 更新系统
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# 安装必要工具
echo "Installing essential tools..."
sudo apt install -y \
    curl \
    wget \
    git \
    vim \
    nano \
    unzip \
    htop \
    tree \
    net-tools \
    dnsutils

# 安装 Docker
echo "Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 将当前用户添加到 docker 组
sudo usermod -aG docker $USER

# 安装 Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
echo "Verifying installations..."
docker --version
docker-compose --version

# 启动并启用 Docker 服务
sudo systemctl start docker
sudo systemctl enable docker

echo "Server setup completed!"
echo "Please logout and login again to apply Docker group membership"
```

### 2. 创建防火墙配置脚本

#### 创建 scripts/setup_firewall.sh (Linux/Mac)
```bash
#!/bin/bash

# 防火墙配置脚本
echo "Configuring firewall..."

# 启用 ufw 防火墙
sudo ufw enable

# 允许 SSH 连接（重要！不要忘记）
sudo ufw allow ssh

# 允许 HTTP 和 HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 允许 Docker 相关端口（如果需要直接访问容器）
# sudo ufw allow 8000/tcp  # FastAPI 后端端口

# 查看防火墙状态
sudo ufw status verbose

echo "Firewall configuration completed!"
```

### 3. 创建应用部署脚本

#### 创建 scripts/deploy_to_server.sh (Linux/Mac)
```bash
#!/bin/bash

# 应用部署脚本
SERVER_USER="deploy"
SERVER_HOST="your-server-ip"  # 替换为你的服务器IP
SERVER_PATH="/opt/tutorial-site"
REMOTE_SCRIPT="/tmp/deploy_remote.sh"

echo "Deploying application to server: $SERVER_HOST"

# 创建远程部署脚本
cat > deploy_temp.sh << 'EOF'
#!/bin/bash

set -e  # 遇到错误时退出

APP_PATH="/opt/tutorial-site"
BACKUP_PATH="/opt/tutorial-site-backup-$(date +%Y%m%d-%H%M%S)"

echo "Starting deployment..."

# 创建备份
if [ -d "$APP_PATH" ]; then
    echo "Creating backup..."
    cp -r "$APP_PATH" "$BACKUP_PATH"
fi

# 创建应用目录
sudo mkdir -p "$APP_PATH"
sudo chown $USER:$USER "$APP_PATH"
cd "$APP_PATH"

# 克隆或更新代码
if [ -d ".git" ]; then
    echo "Updating code from repository..."
    git pull
else
    echo "Cloning repository..."
    # 替换为你的实际仓库地址
    git clone https://github.com/your-username/flutter-fast.git .
fi

# 构建 Flutter Web 前端
echo "Building Flutter Web frontend..."
cd frontend
flutter build web --release
cd ..

# 构建并启动 Docker 服务
echo "Building and starting Docker services..."
docker-compose -f docker-compose.prod.yml up -d --build

# 等待服务启动
echo "Waiting for services to start..."
sleep 15

# 检查服务状态
echo "Checking service status..."
docker-compose -f docker-compose.prod.yml ps

# 测试服务
echo "Testing services..."
curl -f http://localhost/health && echo "Frontend is healthy"
curl -f http://localhost/api/health && echo "Backend is healthy"

echo "Deployment completed successfully!"
EOF

# 传输部署脚本到服务器
echo "Transferring deployment script..."
scp deploy_temp.sh "$SERVER_USER@$SERVER_HOST:$REMOTE_SCRIPT"

# 在服务器上执行部署脚本
echo "Executing deployment on server..."
ssh "$SERVER_USER@$SERVER_HOST" "chmod +x $REMOTE_SCRIPT && $REMOTE_SCRIPT"

# 清理本地临时文件
rm deploy_temp.sh

echo "Remote deployment completed!"
```

### 4. 创建服务器健康检查脚本

#### 创建 scripts/server_health_check.sh (Linux/Mac)
```bash
#!/bin/bash

# 服务器健康检查脚本
SERVER_USER="deploy"
SERVER_HOST="your-server-ip"  # 替换为你的服务器IP

echo "Performing server health check..."

# 检查服务器连通性
echo "Checking server connectivity..."
ping -c 3 "$SERVER_HOST" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Cannot ping server"
    exit 1
else
    echo "✅ Server is reachable"
fi

# 检查 SSH 连接
echo "Checking SSH connection..."
ssh "$SERVER_USER@$SERVER_HOST" "echo 'SSH connection successful'" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Cannot establish SSH connection"
    exit 1
else
    echo "✅ SSH connection successful"
fi

# 检查 Docker 服务
echo "Checking Docker service..."
DOCKER_STATUS=$(ssh "$SERVER_USER@$SERVER_HOST" "systemctl is-active docker")
if [ "$DOCKER_STATUS" != "active" ]; then
    echo "❌ Docker service is not active"
else
    echo "✅ Docker service is active"
fi

# 检查应用服务
echo "Checking application services..."
ssh "$SERVER_USER@$SERVER_HOST" "cd /opt/tutorial-site && docker-compose -f docker-compose.prod.yml ps" || echo "Failed to check services"

# 检查端口连通性
echo "Checking port connectivity..."
nc -zv "$SERVER_HOST" 80 > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Port 80 is not accessible"
else
    echo "✅ Port 80 is accessible"
fi

nc -zv "$SERVER_HOST" 443 > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Port 443 is not accessible"
else
    echo "✅ Port 443 is accessible"
fi

# 检查 HTTP 响应
echo "Checking HTTP response..."
HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "http://$SERVER_HOST/health")
if [ "$HTTP_RESPONSE" = "200" ]; then
    echo "✅ HTTP health check passed"
else
    echo "❌ HTTP health check failed (status: $HTTP_RESPONSE)"
fi

echo "Server health check completed!"
```

### 5. 创建日志查看脚本

#### 创建 scripts/view_logs.sh (Linux/Mac)
```bash
#!/bin/bash

# 日志查看脚本
SERVER_USER="deploy"
SERVER_HOST="your-server-ip"  # 替换为你的服务器IP
SERVICE_NAME=${1:-"all"}  # 默认查看所有服务日志

echo "Viewing logs for service: $SERVICE_NAME"

case $SERVICE_NAME in
    "backend")
        ssh "$SERVER_USER@$SERVER_HOST" "cd /opt/tutorial-site && docker-compose -f docker-compose.prod.yml logs -f --tail=100 backend"
        ;;
    "nginx")
        ssh "$SERVER_USER@$SERVER_HOST" "cd /opt/tutorial-site && docker-compose -f docker-compose.prod.yml logs -f --tail=100 nginx"
        ;;
    "all"|*)
        ssh "$SERVER_USER@$SERVER_HOST" "cd /opt/tutorial-site && docker-compose -f docker-compose.prod.yml logs -f --tail=50"
        ;;
esac
```

### 6. 创建备份脚本

#### 创建 scripts/backup_server.sh (Linux/Mac)
```bash
#!/bin/bash

# 服务器备份脚本
SERVER_USER="deploy"
SERVER_HOST="your-server-ip"  # 替换为你的服务器IP
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d-%H%M%S)

echo "Creating server backup..."

# 创建本地备份目录
mkdir -p "$BACKUP_DIR"

# 备份 Docker 卷
echo "Backing up Docker volumes..."
ssh "$SERVER_USER@$SERVER_HOST" "cd /opt/tutorial-site && docker-compose -f docker-compose.prod.yml exec backend sqlite3 /app/tutorial.db '.backup /tmp/tutorial_backup.db'"
ssh "$SERVER_USER@$SERVER_HOST" "cd /opt/tutorial-site && docker-compose -f docker-compose.prod.yml cp backend:/tmp/tutorial_backup.db /tmp/tutorial_backup_$DATE.db"
scp "$SERVER_USER@$SERVER_HOST:/tmp/tutorial_backup_$DATE.db" "$BACKUP_DIR/"

# 备份应用代码
echo "Backing up application code..."
ssh "$SERVER_USER@$SERVER_HOST" "cd /opt && tar -czf tutorial-site-backup-$DATE.tar.gz tutorial-site"
scp "$SERVER_USER@$SERVER_HOST:/opt/tutorial-site-backup-$DATE.tar.gz" "$BACKUP_DIR/"

# 删除服务器上的临时文件
ssh "$SERVER_USER@$SERVER_HOST" "rm /tmp/tutorial_backup_$DATE.db /opt/tutorial-site-backup-$DATE.tar.gz"

echo "Backup completed!"
echo "Backup files are located in: $BACKUP_DIR"
ls -lh "$BACKUP_DIR"
```

### 7. 创建恢复脚本

#### 创建 scripts/restore_backup.sh (Linux/Mac)
```bash
#!/bin/bash

# 备份恢复脚本
SERVER_USER="deploy"
SERVER_HOST="your-server-ip"  # 替换为你的服务器IP
BACKUP_FILE=${1:-""}

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup-file-path>"
    echo "Available backups:"
    ls -lh ./backups/
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "Restoring backup: $BACKUP_FILE"

# 传输备份文件到服务器
echo "Transferring backup file to server..."
scp "$BACKUP_FILE" "$SERVER_USER@$SERVER_HOST:/tmp/"

# 在服务器上执行恢复操作
BACKUP_FILENAME=$(basename "$BACKUP_FILE")
echo "Restoring on server..."
ssh "$SERVER_USER@$SERVER_HOST" "
    cd /opt &&
    # 停止服务
    cd tutorial-site && docker-compose -f docker-compose.prod.yml down &&
    cd .. &&
    # 恢复备份
    tar -xzf /tmp/$BACKUP_FILENAME &&
    # 重启服务
    cd tutorial-site && docker-compose -f docker-compose.prod.yml up -d
"

# 清理临时文件
ssh "$SERVER_USER@$SERVER_HOST" "rm /tmp/$BACKUP_FILENAME"

echo "Backup restoration completed!"
```

### 8. 创建系统监控脚本

#### 创建 scripts/monitor_server.sh (Linux/Mac)
```bash
#!/bin/bash

# 服务器监控脚本
SERVER_USER="deploy"
SERVER_HOST="your-server-ip"  # 替换为你的服务器IP

echo "Monitoring server: $SERVER_HOST"

# 服务器基本信息
echo "=== Server Information ==="
ssh "$SERVER_USER@$SERVER_HOST" "hostnamectl"

# CPU 和内存使用情况
echo "=== CPU and Memory Usage ==="
ssh "$SERVER_USER@$SERVER_HOST" "top -bn1 | head -20"

# 磁盘使用情况
echo "=== Disk Usage ==="
ssh "$SERVER_USER@$SERVER_HOST" "df -h"

# Docker 容器状态
echo "=== Docker Containers ==="
ssh "$SERVER_USER@$SERVER_HOST" "docker ps -a"

# 应用服务状态
echo "=== Application Services ==="
ssh "$SERVER_USER@$SERVER_HOST" "cd /opt/tutorial-site && docker-compose -f docker-compose.prod.yml ps"

# 网络连接
echo "=== Network Connections ==="
ssh "$SERVER_USER@$SERVER_HOST" "ss -tuln"

# 最近的系统日志
echo "=== Recent System Logs ==="
ssh "$SERVER_USER@$SERVER_HOST" "journalctl -n 20"

echo "Server monitoring completed!"
```

### 9. 创建环境变量配置文件

#### 创建 .env.example
```env
# 应用环境变量示例文件
# 复制此文件为 .env 并填写实际值

# 数据库配置
DATABASE_URL=sqlite:///./tutorial.db

# API 配置
API_HOST=0.0.0.0
API_PORT=8000

# 前端配置
FRONTEND_PORT=80

# SSL 配置（如果使用 HTTPS）
SSL_CERTIFICATE_PATH=
SSL_CERTIFICATE_KEY_PATH=

# GitHub 集成（可选）
GITHUB_TOKEN=

# 其他配置
DEBUG=False
LOG_LEVEL=info
```

## 服务器部署步骤

### 1. 服务器准备
```bash
# 运行服务器初始化脚本
./scripts/server_setup.sh
```

### 2. 防火墙配置
```bash
# 配置防火墙规则
./scripts/setup_firewall.sh
```

### 3. 应用部署
```bash
# 部署应用到服务器
./scripts/deploy_to_server.sh
```

### 4. 健康检查
```bash
# 检查服务器健康状态
./scripts/server_health_check.sh
```

## 易错点及解决方案

### 1. 权限问题
**问题：**
无法执行 Docker 命令

**解决方案：**
将用户添加到 docker 组并重新登录

### 2. 端口冲突
**问题：**
端口已被占用导致部署失败

**解决方案：**
检查端口使用情况，停止冲突服务或更改端口

### 3. 磁盘空间不足
**问题：**
Docker 镜像和日志占用过多空间

**解决方案：**
清理不需要的镜像和日志，扩展磁盘空间

### 4. 网络连接问题
**问题：**
服务器无法访问外部网络

**解决方案：**
检查网络配置和 DNS 设置

## 今日任务检查清单
- [ ] 准备服务器环境
- [ ] 安装 Docker 和 Docker Compose
- [ ] 配置防火墙规则
- [ ] 部署完整应用栈
- [ ] 验证部署结果

## 扩展阅读
- [Ubuntu Server 指南](https://ubuntu.com/server/docs)
- [Docker 生产环境部署](https://docs.docker.com/go/production-checklist/)
- [服务器安全最佳实践](https://ubuntu.com/server/docs/security)