# Day 23 详细学习计划：Nginx 与服务器配置

## 学习目标
- 学习 Nginx 基础配置
- 配置反向代理
- 实现静态文件服务
- 配置 HTTPS 支持

## 知识点详解

### 1. Nginx 基础
**Nginx 简介：**
- 高性能 HTTP 服务器和反向代理服务器
- 事件驱动架构，高并发处理能力强
- 轻量级，内存消耗少

**核心概念：**
- Server Blocks（类似 Apache 的 Virtual Hosts）
- Location Blocks（URL 匹配规则）
- Upstream（上游服务器定义）

### 2. 反向代理配置
**作用：**
- 隐藏后端服务器
- 负载均衡
- SSL 终止
- 缓存静态内容

**配置要点：**
- proxy_pass 指令
- 请求头转发
- 响应头处理

### 3. 静态文件服务
**优势：**
- 直接从磁盘提供文件
- 高效处理静态资源
- 支持缓存和压缩

**配置项：**
- root 和 alias 指令
- try_files 指令
- MIME 类型配置

## 练习代码

### 1. 创建基础 Nginx 配置文件

#### 创建 nginx/nginx.conf
```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/doc/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 4096;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    include /etc/nginx/conf.d/*.conf;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    server {
        listen 80;
        server_name _;

        # Serve static files
        location / {
            root /var/www/html;
            index index.html index.htm;
            try_files $uri $uri/ /index.html;
        }

        # Proxy API requests to FastAPI backend
        location /api/ {
            proxy_pass http://backend:8000/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check endpoint
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }

        # Error pages
        error_page 404 /404.html;
        location = /404.html {
            internal;
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
            internal;
        }
    }
}
```

### 2. 创建 Docker 化的 Nginx 配置

#### 创建 nginx/docker-nginx.conf
```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    # MIME types
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                   '$status $body_bytes_sent "$http_referer" '
                   '"$http_user_agent" "$http_x_forwarded_for"';
    
    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log;

    # Basic settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    # Server block
    server {
        listen 80;
        server_name localhost;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

        # Static files for Flutter Web
        location / {
            root /usr/share/nginx/html;
            index index.html index.htm;
            try_files $uri $uri/ /index.html;
            
            # Cache static assets
            location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
                expires 1y;
                add_header Cache-Control "public, immutable";
            }
        }

        # API proxy to FastAPI backend
        location /api/ {
            proxy_pass http://backend:8000/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Timeout settings
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }

        # Health check endpoint
        location = /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }

        # Error pages
        error_page 404 /404.html;
        location = /404.html {
            root /usr/share/nginx/html;
            internal;
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
            root /usr/share/nginx/html;
            internal;
        }
    }
}
```

### 3. 更新 docker-compose.yml

#### 更新 docker-compose.yml
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend/tutorial.db:/app/tutorial.db
      - ./backend/logs:/app/logs
    environment:
      - HOST=0.0.0.0
      - PORT=8000
    restart: unless-stopped
    networks:
      - app-network

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    volumes:
      - ./frontend/build/web:/usr/share/nginx/html
      - ./nginx/docker-nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - backend
    restart: unless-stopped
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### 4. 创建独立的 docker-compose 部署文件

#### 创建 docker-compose.prod.yml
```yaml
version: '3.8'

services:
  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    volumes:
      - backend_data:/app
    environment:
      - HOST=0.0.0.0
      - PORT=8000
    restart: unless-stopped
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./frontend/build/web:/usr/share/nginx/html
      - ./nginx/docker-nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - nginx_logs:/var/log/nginx
    depends_on:
      - backend
    restart: unless-stopped
    networks:
      - app-network

volumes:
  backend_data:
  nginx_logs:

networks:
  app-network:
    driver: bridge
```

### 5. 创建 Nginx 日志分析脚本

#### 创建 scripts/analyze_nginx_logs.sh (Linux/Mac)
```bash
#!/bin/bash

LOG_FILE="./nginx/logs/access.log"

if [ ! -f "$LOG_FILE" ]; then
    echo "Log file not found: $LOG_FILE"
    exit 1
fi

echo "=== Nginx Log Analysis ==="
echo "Date: $(date)"
echo ""

echo "=== Total Requests ==="
wc -l < "$LOG_FILE"

echo "=== Top 10 IP Addresses ==="
awk '{print $1}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -10

echo "=== Top 10 Requested URLs ==="
awk '{print $7}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -10

echo "=== HTTP Status Codes ==="
awk '{print $9}' "$LOG_FILE" | sort | uniq -c | sort -nr

echo "=== Top 10 User Agents ==="
awk -F'"' '{print $6}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -10

echo "=== Requests per Hour ==="
awk '{print $4}' "$LOG_FILE" | cut -d: -f2 | sort | uniq -c | sort -nr
```

### 6. 创建 Nginx 配置测试脚本

#### 创建 scripts/test_nginx_config.sh (Linux/Mac)
```bash
#!/bin/bash

echo "Testing Nginx Configuration..."

# 测试配置文件语法
docker run --rm \
  -v "$(pwd)/nginx/docker-nginx.conf:/etc/nginx/nginx.conf:ro" \
  nginx:alpine \
  nginx -t

if [ $? -eq 0 ]; then
    echo "✅ Nginx configuration is valid"
else
    echo "❌ Nginx configuration has errors"
    exit 1
fi

echo "Testing basic connectivity..."

# 启动测试容器
echo "Starting test containers..."
docker-compose -f docker-compose.prod.yml up -d

# 等待服务启动
sleep 10

# 测试 Nginx 服务
echo "Testing Nginx service..."
curl -f http://localhost/health || echo "Nginx health check failed"

# 测试 API 代理
echo "Testing API proxy..."
curl -f http://localhost/api/health || echo "API proxy test failed"

# 停止测试容器
echo "Stopping test containers..."
docker-compose -f docker-compose.prod.yml down

echo "Nginx configuration test completed!"
```

### 7. 创建 SSL 配置模板

#### 创建 nginx/ssl-config-template.conf
```nginx
# SSL Configuration Template
# This file should be customized with actual SSL certificates

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL certificate files
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/private.key;

    # SSL security settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Static files for Flutter Web
    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
        
        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # API proxy to FastAPI backend
    location /api/ {
        proxy_pass http://backend:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check endpoint
    location = /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    return 301 https://$server_name$request_uri;
}
```

### 8. 创建部署脚本

#### 创建 scripts/deploy.sh (Linux/Mac)
```bash
#!/bin/bash

echo "Starting deployment process..."

# 1. 构建 Flutter Web 前端
echo "Building Flutter Web frontend..."
(cd frontend && flutter build web --release)

# 2. 构建后端 Docker 镜像
echo "Building backend Docker image..."
docker build -t tutorial-backend ./backend

# 3. 启动服务
echo "Starting services with docker-compose..."
docker-compose -f docker-compose.prod.yml up -d

# 4. 检查服务状态
echo "Checking service status..."
sleep 10
docker-compose -f docker-compose.prod.yml ps

# 5. 测试服务
echo "Testing deployed services..."
curl -f http://localhost/health && echo "Frontend is healthy"
curl -f http://localhost/api/health && echo "Backend is healthy"

echo "Deployment completed!"
echo "Visit http://localhost to access your application"
```

## Nginx 常用命令

### 测试配置文件
```bash
nginx -t
```

### 重新加载配置
```bash
nginx -s reload
```

### 启动 Nginx
```bash
nginx
```

### 停止 Nginx
```bash
nginx -s stop
```

## 易错点及解决方案

### 1. 权限问题
**问题：**
Nginx 无法访问静态文件

**解决方案：**
确保文件权限正确，通常需要 644 权限

### 2. 代理配置错误
**问题：**
API 请求返回 502 错误

**解决方案：**
检查 upstream 配置和服务是否正常运行

### 3. 路径匹配问题
**问题：**
SPA 路由刷新后 404

**解决方案：**
使用 try_files 指令重定向到 index.html

### 4. SSL 配置错误
**问题：**
HTTPS 无法正常工作

**解决方案：**
确保证书文件路径正确，权限设置合适

## 今日任务检查清单
- [ ] 创建 Nginx 配置文件
- [ ] 配置反向代理规则
- [ ] 设置静态文件服务
- [ ] 更新 docker-compose 配置
- [ ] 测试部署配置

## 扩展阅读
- [Nginx 官方文档](https://nginx.org/en/docs/)
- [Docker Compose 文档](https://docs.docker.com/compose/)
- [SSL/TLS 配置最佳实践](https://ssl-config.mozilla.org/)