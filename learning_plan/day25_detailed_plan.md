# Day 25 详细学习计划：域名配置与 HTTPS 证书申请

## 学习目标
- 学习域名购买和配置
- 申请免费 SSL 证书
- 配置 HTTPS 支持
- 实现 HTTP 到 HTTPS 重定向

## 知识点详解

### 1. 域名基础知识
**域名结构：**
- 顶级域名(TLD)：.com, .org, .net 等
- 二级域名：google.com 中的 google
- 子域名：mail.google.com 中的 mail

**DNS 记录类型：**
- A 记录：域名指向 IPv4 地址
- AAAA 记录：域名指向 IPv6 地址
- CNAME 记录：域名指向另一个域名
- MX 记录：邮件服务器记录

### 2. SSL/TLS 证书
**证书类型：**
- DV (Domain Validation)：域名验证
- OV (Organization Validation)：组织验证
- EV (Extended Validation)：扩展验证

**证书颁发机构：**
- Let's Encrypt：免费，自动化
- 商业 CA：付费，提供更多功能

### 3. HTTPS 配置
**配置要素：**
- SSL 证书文件
- 私钥文件
- 证书链文件
- 安全协议和加密套件

## 练习代码

### 1. 创建 SSL 证书申请脚本

#### 创建 scripts/request_ssl_cert.sh (Linux/Mac)
```bash
#!/bin/bash

# SSL 证书申请脚本 (使用 Let's Encrypt)
DOMAIN=${1:-"yourdomain.com"}  # 替换为你的域名
EMAIL=${2:-"admin@yourdomain.com"}  # 替换为你的邮箱
WEBROOT_PATH="/var/www/html"

echo "Requesting SSL certificate for domain: $DOMAIN"

# 安装 Certbot (Let's Encrypt 客户端)
echo "Installing Certbot..."
sudo apt update
sudo apt install -y certbot

# 如果使用 standalone 模式（临时停止 Web 服务器）
echo "Requesting certificate using standalone mode..."
sudo certbot certonly \
  --standalone \
  --preferred-challenges http \
  --email "$EMAIL" \
  --agree-tos \
  --domain "$DOMAIN" \
  --domain "www.$DOMAIN" \
  --non-interactive

# 检查证书是否申请成功
if [ $? -eq 0 ]; then
    echo "✅ SSL certificate successfully requested!"
    echo "Certificate location: /etc/letsencrypt/live/$DOMAIN/"
    
    # 显示证书信息
    sudo certbot certificates
    
    # 设置自动续期
    echo "Setting up automatic renewal..."
    sudo crontab -l | { cat; echo "0 12 * * * /usr/bin/certbot renew --quiet"; } | sudo crontab -
    
    echo "✅ Automatic renewal configured"
else
    echo "❌ Failed to request SSL certificate"
    exit 1
fi
```

### 2. 创建使用 Docker 的 SSL 证书申请脚本

#### 创建 scripts/request_ssl_docker.sh (Linux/Mac)
```bash
#!/bin/bash

# 使用 Docker 的 SSL 证书申请脚本
DOMAIN=${1:-"yourdomain.com"}  # 替换为你的域名
EMAIL=${2:-"admin@yourdomain.com"}  # 替换为你的邮箱

echo "Requesting SSL certificate for domain: $DOMAIN using Docker"

# 拉取 Certbot 镜像
echo "Pulling Certbot Docker image..."
docker pull certbot/certbot

# 创建证书目录
sudo mkdir -p /etc/letsencrypt
sudo mkdir -p /var/www/certbot

# 运行 Certbot 获取证书
echo "Requesting certificate..."
docker run --rm \
  -v "/etc/letsencrypt:/etc/letsencrypt" \
  -v "/var/www/certbot:/var/www/certbot" \
  certbot/certbot \
  certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email "$EMAIL" \
  --agree-tos \
  --no-eff-email \
  --domain "$DOMAIN" \
  --domain "www.$DOMAIN"

# 检查证书是否申请成功
if [ $? -eq 0 ]; then
    echo "✅ SSL certificate successfully requested!"
    echo "Certificate location: /etc/letsencrypt/live/$DOMAIN/"
    
    # 显示证书信息
    docker run --rm \
      -v "/etc/letsencrypt:/etc/letsencrypt" \
      certbot/certbot \
      certificates
    
    echo "✅ Certificate ready for use with Docker"
else
    echo "❌ Failed to request SSL certificate"
    exit 1
fi
```

### 3. 更新 Nginx HTTPS 配置

#### 创建 nginx/https-nginx.conf
```nginx
events {
    worker_connections 1024;
}

http {
    # 上游服务器配置
    upstream backend {
        server backend:8000;
    }

    # MIME 类型
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # 日志格式
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                   '$status $body_bytes_sent "$http_referer" '
                   '"$http_user_agent" "$http_x_forwarded_for"';
    
    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log;

    # 基本设置
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Gzip 压缩
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

    # HTTP 服务器块 (重定向到 HTTPS)
    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        
        # Let's Encrypt 验证路径
        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }
        
        # 其他所有请求重定向到 HTTPS
        location / {
            return 301 https://$host$request_uri;
        }
    }

    # HTTPS 服务器块
    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        # SSL 证书配置
        ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
        
        # SSL 安全设置
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

        # 安全头
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # 静态文件服务 (Flutter Web)
        location / {
            root /usr/share/nginx/html;
            index index.html index.htm;
            try_files $uri $uri/ /index.html;
            
            # 缓存静态资源
            location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
                expires 1y;
                add_header Cache-Control "public, immutable";
            }
        }

        # API 代理到 FastAPI 后端
        location /api/ {
            proxy_pass http://backend:8000/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # 超时设置
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }

        # 健康检查端点
        location = /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }

        # 错误页面
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

### 4. 创建 SSL 证书续期脚本

#### 创建 scripts/renew_ssl_cert.sh (Linux/Mac)
```bash
#!/bin/bash

# SSL 证书续期脚本
echo "Renewing SSL certificates..."

# 使用 Certbot 续期证书
sudo certbot renew --quiet

# 检查续期结果
if [ $? -eq 0 ]; then
    echo "✅ SSL certificates renewed successfully"
    
    # 重新加载 Nginx 配置以使用新证书
    echo "Reloading Nginx configuration..."
    sudo systemctl reload nginx
    
    if [ $? -eq 0 ]; then
        echo "✅ Nginx reloaded successfully"
    else
        echo "❌ Failed to reload Nginx"
    fi
else
    echo "❌ Failed to renew SSL certificates"
fi

# 显示证书状态
echo "Current certificate status:"
sudo certbot certificates
```

### 5. 创建 Docker 化的 SSL 续期脚本

#### 创建 scripts/renew_ssl_docker.sh (Linux/Mac)
```bash
#!/bin/bash

# Docker 化的 SSL 证书续期脚本
echo "Renewing SSL certificates using Docker..."

# 运行 Certbot 续期
docker run --rm \
  -v "/etc/letsencrypt:/etc/letsencrypt" \
  -v "/var/www/certbot:/var/www/certbot" \
  certbot/certbot \
  renew

# 检查续期结果
if [ $? -eq 0 ]; then
    echo "✅ SSL certificates renewed successfully"
    
    # 重新启动 Nginx 容器以加载新证书
    echo "Restarting Nginx container..."
    docker-compose -f docker-compose.prod.yml restart nginx
    
    if [ $? -eq 0 ]; then
        echo "✅ Nginx container restarted successfully"
    else
        echo "❌ Failed to restart Nginx container"
    fi
else
    echo "❌ Failed to renew SSL certificates"
fi

# 显示证书状态
echo "Current certificate status:"
docker run --rm \
  -v "/etc/letsencrypt:/etc/letsencrypt" \
  certbot/certbot \
  certificates
```

### 6. 创建 HTTPS 测试脚本

#### 创建 scripts/test_https.sh (Linux/Mac)
```bash
#!/bin/bash

# HTTPS 配置测试脚本
DOMAIN=${1:-"yourdomain.com"}  # 替换为你的域名

echo "Testing HTTPS configuration for: $DOMAIN"

# 测试 HTTPS 连接
echo "1. Testing HTTPS connectivity..."
curl -f https://"$DOMAIN"/health > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ HTTPS connectivity test passed"
else
    echo "❌ HTTPS connectivity test failed"
fi

# 测试 HTTP 重定向
echo "2. Testing HTTP to HTTPS redirection..."
HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://"$DOMAIN"/health)
if [ "$HTTP_RESPONSE" = "301" ]; then
    echo "✅ HTTP to HTTPS redirection working"
else
    echo "❌ HTTP to HTTPS redirection not working (status: $HTTP_RESPONSE)"
fi

# 检查 SSL 证书有效性
echo "3. Checking SSL certificate validity..."
openssl s_client -connect "$DOMAIN":443 -servername "$DOMAIN" < /dev/null 2>/dev/null | openssl x509 -noout -dates
if [ $? -eq 0 ]; then
    echo "✅ SSL certificate is valid"
else
    echo "❌ SSL certificate validation failed"
fi

# 测试安全头
echo "4. Testing security headers..."
curl -s -D - https://"$DOMAIN"/ | grep -E "(Strict-Transport-Security|X-Frame-Options|X-Content-Type-Options)"
if [ $? -eq 0 ]; then
    echo "✅ Security headers present"
else
    echo "⚠️  Some security headers may be missing"
fi

echo "HTTPS testing completed!"
```

### 7. 创建自动续期 Cron 任务脚本

#### 创建 scripts/setup_auto_renewal.sh (Linux/Mac)
```bash
#!/bin/bash

# 设置自动续期 Cron 任务
echo "Setting up automatic SSL certificate renewal..."

# 创建续期脚本
sudo tee /usr/local/bin/renew-ssl-cert.sh > /dev/null << 'EOF'
#!/bin/bash
# SSL 证书自动续期脚本

# 续期证书
/usr/bin/certbot renew --quiet

# 如果证书有更新，则重新加载 Nginx
if [ $? -eq 0 ]; then
    /usr/bin/systemctl reload nginx
fi
EOF

# 设置脚本权限
sudo chmod +x /usr/local/bin/renew-ssl-cert.sh

# 添加到 Crontab (每月第一个周日凌晨2点执行)
(crontab -l 2>/dev/null; echo "0 2 1 * * /usr/local/bin/renew-ssl-cert.sh") | crontab -

echo "✅ Automatic renewal scheduled"
echo "Next renewal will run on the first Sunday of each month at 2:00 AM"

# 显示当前的 Crontab
echo "Current crontab:"
crontab -l
```

### 8. 创建域名配置检查脚本

#### 创建 scripts/check_domain_config.sh (Linux/Mac)
```bash
#!/bin/bash

# 域名配置检查脚本
DOMAIN=${1:-"yourdomain.com"}  # 替换为你的域名

echo "Checking domain configuration for: $DOMAIN"

# 检查 A 记录
echo "1. Checking A record..."
A_RECORD=$(dig +short "$DOMAIN" A)
if [ -n "$A_RECORD" ]; then
    echo "✅ A record found: $A_RECORD"
else
    echo "❌ No A record found for $DOMAIN"
fi

# 检查 www 子域名 A 记录
echo "2. Checking www.$DOMAIN A record..."
WWW_A_RECORD=$(dig +short "www.$DOMAIN" A)
if [ -n "$WWW_A_RECORD" ]; then
    echo "✅ www.$DOMAIN A record found: $WWW_A_RECORD"
else
    echo "❌ No A record found for www.$DOMAIN"
fi

# 检查 MX 记录（可选）
echo "3. Checking MX records..."
MX_RECORDS=$(dig +short "$DOMAIN" MX)
if [ -n "$MX_RECORDS" ]; then
    echo "ℹ️  MX records found:"
    echo "$MX_RECORDS"
else
    echo "ℹ️  No MX records found (optional for web-only sites)"
fi

# 检查 SPF 记录（可选）
echo "4. Checking SPF records..."
SPF_RECORD=$(dig +short "$DOMAIN" TXT | grep "v=spf1")
if [ -n "$SPF_RECORD" ]; then
    echo "ℹ️  SPF record found: $SPF_RECORD"
else
    echo "ℹ️  No SPF record found (recommended for email)"
fi

# 检查域名解析时间
echo "5. Checking DNS resolution time..."
RESOLUTION_TIME=$(dig "$DOMAIN" | grep "Query time" | awk '{print $4}')
echo "ℹ️  DNS resolution time: ${RESOLUTION_TIME}ms"

echo "Domain configuration check completed!"
```

### 9. 更新 docker-compose 配置支持 HTTPS

#### 更新 docker-compose.prod.yml
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
      - ./nginx/https-nginx.conf:/etc/nginx/nginx.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
      - /var/www/certbot:/var/www/certbot
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

## SSL 证书管理命令

### 手动申请证书
```bash
sudo certbot certonly --standalone --preferred-challenges http --email admin@yourdomain.com --agree-tos --domain yourdomain.com
```

### 检查证书状态
```bash
sudo certbot certificates
```

### 手动续期证书
```bash
sudo certbot renew
```

### 测试续期过程
```bash
sudo certbot renew --dry-run
```

## 易错点及解决方案

### 1. 域名解析问题
**问题：**
证书申请失败，因为域名无法解析

**解决方案：**
确保 DNS 记录已正确配置并已传播

### 2. 端口占用问题
**问题：**
Let's Encrypt 验证失败，因为 80 端口被占用

**解决方案：**
临时停止 Web 服务器或使用 webroot 模式

### 3. 权限问题
**问题：**
无法访问证书文件

**解决方案：**
确保 Nginx 进程有权限读取证书文件

### 4. 证书续期失败
**问题：**
自动续期失败导致证书过期

**解决方案：**
设置监控和警报，定期手动检查证书状态

## 今日任务检查清单
- [ ] 配置域名 DNS 记录
- [ ] 申请 SSL 证书
- [ ] 配置 Nginx HTTPS 支持
- [ ] 实现 HTTP 到 HTTPS 重定向
- [ ] 设置自动续期机制
- [ ] 测试 HTTPS 配置

## 扩展阅读
- [Let's Encrypt 官方文档](https://letsencrypt.org/docs/)
- [Certbot 使用指南](https://certbot.eff.org/docs/)
- [SSL/TLS 最佳实践](https://ssl-config.mozilla.org/)
- [DNS 记录类型详解](https://www.cloudflare.com/learning/dns/dns-records/)