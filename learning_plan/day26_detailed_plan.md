# Day 26 详细学习计划：生产环境优化与监控

## 学习目标
- 优化应用性能
- 配置应用监控
- 实施日志管理
- 设置告警机制

## 知识点详解

### 1. 性能优化策略
**前端优化：**
- 代码分割和懒加载
- 资源压缩和缓存
- 图片优化
- 减少 HTTP 请求

**后端优化：**
- 数据库查询优化
- API 响应缓存
- 连接池配置
- 异步处理

### 2. 监控系统
**监控指标：**
- 系统资源使用率（CPU、内存、磁盘）
- 应用性能指标（响应时间、吞吐量）
- 错误率和异常情况
- 用户行为指标

**监控工具：**
- Prometheus + Grafana
- ELK Stack (Elasticsearch, Logstash, Kibana)
- 自建监控脚本

### 3. 日志管理
**日志级别：**
- DEBUG：调试信息
- INFO：一般信息
- WARNING：警告信息
- ERROR：错误信息
- CRITICAL：严重错误

**日志轮转：**
- 按时间轮转
- 按大小轮转
- 压缩旧日志

## 练习代码

### 1. 创建性能监控脚本

#### 创建 scripts/performance_monitor.sh (Linux/Mac)
```bash
#!/bin/bash

# 性能监控脚本
echo "=== Application Performance Monitor ==="
echo "Timestamp: $(date)"
echo ""

# 系统资源使用情况
echo "=== System Resources ==="
echo "CPU Usage:"
top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1

echo "Memory Usage:"
free -h | grep "Mem"

echo "Disk Usage:"
df -h /

# Docker 容器资源使用情况
echo ""
echo "=== Docker Container Resources ==="
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

# 应用响应时间测试
echo ""
echo "=== Application Response Time ==="
DOMAIN=${1:-"localhost"}

# 测试首页响应时间
HOMEPAGE_TIME=$(curl -s -o /dev/null -w "%{time_total}" "http://$DOMAIN/")
echo "Homepage response time: ${HOMEPAGE_TIME}s"

# 测试 API 响应时间
API_TIME=$(curl -s -o /dev/null -w "%{time_total}" "http://$DOMAIN/api/health")
echo "API response time: ${API_TIME}s"

# 测试 HTTPS (如果配置了)
HTTPS_TIME=$(curl -s -o /dev/null -w "%{time_total}" "https://$DOMAIN/" 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "HTTPS homepage response time: ${HTTPS_TIME}s"
fi

# 数据库连接测试
echo ""
echo "=== Database Health ==="
docker-compose -f docker-compose.prod.yml exec backend python -c "
import sqlite3
try:
    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()
    cursor.execute('SELECT 1')
    print('✅ Database connection: OK')
    conn.close()
except Exception as e:
    print(f'❌ Database connection: FAILED - {e}')
"

echo ""
echo "=== Performance Monitoring Completed ==="
```

### 2. 创建日志分析脚本

#### 创建 scripts/log_analyzer.sh (Linux/Mac)
```bash
#!/bin/bash

# 日志分析脚本
LOG_DIR=${1:-"/var/log"}
OUTPUT_FILE=${2:-"log_analysis_$(date +%Y%m%d_%H%M%S).txt"}

echo "Analyzing logs and saving to $OUTPUT_FILE"

{
    echo "=== Log Analysis Report ==="
    echo "Generated at: $(date)"
    echo ""
    
    echo "=== Nginx Access Logs Summary ==="
    if [ -f "$LOG_DIR/nginx/access.log" ]; then
        echo "Total requests: $(wc -l < $LOG_DIR/nginx/access.log)"
        echo "Unique visitors: $(awk '{print $1}' $LOG_DIR/nginx/access.log | sort -u | wc -l)"
        echo "Top 10 requested URLs:"
        awk '{print $7}' $LOG_DIR/nginx/access.log | sort | uniq -c | sort -nr | head -10
        echo ""
        echo "HTTP Status Codes:"
        awk '{print $9}' $LOG_DIR/nginx/access.log | sort | uniq -c | sort -nr
    else
        echo "Nginx access log not found"
    fi
    
    echo ""
    echo "=== Nginx Error Logs ==="
    if [ -f "$LOG_DIR/nginx/error.log" ]; then
        echo "Recent errors:"
        tail -20 $LOG_DIR/nginx/error.log
        echo ""
        echo "Error count by type:"
        grep -o "^\[error\]" $LOG_DIR/nginx/error.log | wc -l
        grep -o "^\[warn\]" $LOG_DIR/nginx/error.log | wc -l
    else
        echo "Nginx error log not found"
    fi
    
    echo ""
    echo "=== Application Logs ==="
    echo "Checking Docker container logs..."
    echo "Backend errors:"
    docker-compose -f docker-compose.prod.yml logs --tail=50 backend | grep -i "error\|exception\|fail" || echo "No errors found"
    
    echo ""
    echo "=== System Logs ==="
    echo "Recent system errors:"
    journalctl -p 3 -n 10 --no-pager
    
    echo ""
    echo "=== Resource Usage ==="
    echo "Current memory usage:"
    free -h
    echo ""
    echo "Current disk usage:"
    df -h
    
} > "$OUTPUT_FILE"

echo "Log analysis completed. Report saved to $OUTPUT_FILE"
```

### 3. 创建日志轮转配置

#### 创建 logrotate 配置文件 /etc/logrotate.d/tutorial-site
```bash
# Tutorial Site Log Rotation Configuration

/var/log/tutorial-site/*.log
/var/log/nginx/*.log
{
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 root root
    sharedscripts
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 `cat /var/run/nginx.pid`
    endscript
}
```

### 4. 创建 Prometheus 监控配置

#### 创建 prometheus/prometheus.yml
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'tutorial-site'
    static_configs:
      - targets: ['localhost:8000']  # FastAPI 应用指标端点
    metrics_path: '/metrics'
    
  - job_name: 'nginx'
    static_configs:
      - targets: ['localhost:9113']  # Nginx Exporter
    
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']  # Node Exporter
```

### 5. 创建 Grafana 仪表板配置

#### 创建 grafana/dashboard.json
```json
{
  "dashboard": {
    "id": null,
    "title": "Tutorial Site Monitoring",
    "timezone": "browser",
    "schemaVersion": 16,
    "version": 0,
    "refresh": "30s",
    "panels": [
      {
        "id": 1,
        "type": "graph",
        "title": "HTTP Requests",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{status}}",
            "refId": "A"
          }
        ]
      },
      {
        "id": 2,
        "type": "singlestat",
        "title": "Current Uptime",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "time() - process_start_time_seconds{job=\"tutorial-site\"}",
            "refId": "A"
          }
        ],
        "format": "s",
        "prefix": "Uptime: "
      },
      {
        "id": 3,
        "type": "graph",
        "title": "System CPU Usage",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "100 - (avg by(instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
            "legendFormat": "CPU Usage",
            "refId": "A"
          }
        ]
      },
      {
        "id": 4,
        "type": "graph",
        "title": "Memory Usage",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100",
            "legendFormat": "Memory Available %",
            "refId": "A"
          }
        ]
      }
    ]
  }
}
```

### 6. 创建健康检查和告警脚本

#### 创建 scripts/health_check.sh (Linux/Mac)
```bash
#!/bin/bash

# 健康检查脚本
DOMAIN=${1:-"localhost"}
ALERT_EMAIL=${2:-"admin@yourdomain.com"}

echo "Performing health check for $DOMAIN"

# 检查服务状态
HEALTH_STATUS=0

# 检查前端
echo "Checking frontend..."
curl -f "http://$DOMAIN/health" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend is unhealthy"
    HEALTH_STATUS=1
fi

# 检查后端 API
echo "Checking backend API..."
curl -f "http://$DOMAIN/api/health" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Backend API is healthy"
else
    echo "❌ Backend API is unhealthy"
    HEALTH_STATUS=1
fi

# 检查数据库
echo "Checking database..."
docker-compose -f docker-compose.prod.yml exec backend python -c "
import sqlite3
try:
    conn = sqlite3.connect('tutorial.db')
    cursor = conn.cursor()
    cursor.execute('SELECT 1')
    print('✅ Database is healthy')
    conn.close()
except Exception as e:
    print(f'❌ Database is unhealthy: {e}')
    exit(1)
" > /dev/null 2>&1

if [ $? -ne 0 ]; then
    HEALTH_STATUS=1
fi

# 检查 Docker 容器
echo "Checking Docker containers..."
docker-compose -f docker-compose.prod.yml ps | grep -q "Up"
if [ $? -eq 0 ]; then
    echo "✅ All containers are running"
else
    echo "❌ Some containers are not running"
    HEALTH_STATUS=1
fi

# 如果健康检查失败，发送告警
if [ $HEALTH_STATUS -ne 0 ]; then
    echo "⚠️  Health check failed! Sending alert..."
    
    # 发送邮件告警（需要配置邮件服务器）
    # echo "Health check failed for $DOMAIN" | mail -s "Application Health Alert" "$ALERT_EMAIL"
    
    # 或者使用 curl 发送到 webhook
    # curl -X POST -H "Content-Type: application/json" -d '{"text":"Health check failed for '"$DOMAIN"'"}' YOUR_WEBHOOK_URL
    
    exit 1
else
    echo "✅ All health checks passed"
fi
```

### 7. 创建自动健康检查 Cron 任务

#### 创建 scripts/setup_health_check.sh (Linux/Mac)
```bash
#!/bin/bash

# 设置自动健康检查
echo "Setting up automatic health checks..."

# 创建健康检查脚本
sudo tee /usr/local/bin/health-check.sh > /dev/null << 'EOF'
#!/bin/bash
# 自动健康检查脚本

DOMAIN="yourdomain.com"
ALERT_EMAIL="admin@yourdomain.com"

# 执行健康检查
cd /opt/tutorial-site
./scripts/health_check.sh "$DOMAIN" "$ALERT_EMAIL"

# 如果检查失败，记录到日志
if [ $? -ne 0 ]; then
    echo "$(date): Health check failed" >> /var/log/tutorial-site/health-check.log
fi
EOF

# 设置脚本权限
sudo chmod +x /usr/local/bin/health-check.sh

# 创建日志目录
sudo mkdir -p /var/log/tutorial-site

# 添加到 Crontab (每5分钟执行一次)
(crontab -l 2>/dev/null; echo "*/5 * * * * /usr/local/bin/health-check.sh") | crontab -

echo "✅ Automatic health checks scheduled"
echo "Health checks will run every 5 minutes"

# 显示当前的 Crontab
echo "Current crontab:"
crontab -l
```

### 8. 创建性能优化配置

#### 更新 nginx/optimized-nginx.conf
```nginx
events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    upstream backend {
        server backend:8000;
        keepalive 32;
    }

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # 日志格式
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                   '$status $body_bytes_sent "$http_referer" '
                   '"$http_user_agent" "$http_x_forwarded_for" "$request_time"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log;

    # 基本优化设置
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    keepalive_requests 100;
    types_hash_max_size 2048;

    # Gzip 压缩优化
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

    # 缓存设置
    open_file_cache max=1000 inactive=20s;
    open_file_cache_valid 30s;
    open_file_cache_min_uses 2;
    open_file_cache_errors on;

    # HTTP 服务器块
    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        
        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }
        
        location / {
            return 301 https://$host$request_uri;
        }
    }

    # HTTPS 服务器块
    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        # SSL 配置
        ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
        
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;

        # 安全头
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # 静态文件服务
        location / {
            root /usr/share/nginx/html;
            index index.html index.htm;
            try_files $uri $uri/ /index.html;
            
            # 静态资源缓存
            location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
                expires 1y;
                add_header Cache-Control "public, immutable";
                add_header Vary Accept-Encoding;
            }
        }

        # API 代理
        location /api/ {
            proxy_pass http://backend/;
            proxy_http_version 1.1;
            proxy_set_header Connection "";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
            
            proxy_cache_valid 200 1h;
            proxy_cache_valid 404 1m;
        }

        # 健康检查
        location = /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
    }
}
```

### 9. 创建资源清理脚本

#### 创建 scripts/cleanup_resources.sh (Linux/Mac)
```bash
#!/bin/bash

# 资源清理脚本
echo "Cleaning up system resources..."

# 清理 Docker 资源
echo "Cleaning Docker resources..."
docker system prune -f
docker volume prune -f
docker image prune -f

# 清理系统日志
echo "Cleaning system logs..."
sudo journalctl --vacuum-time=7d

# 清理应用日志
echo "Cleaning application logs..."
sudo find /var/log/tutorial-site -name "*.log" -mtime +30 -delete

# 清理临时文件
echo "Cleaning temporary files..."
sudo rm -rf /tmp/* 2>/dev/null
sudo rm -rf /var/tmp/* 2>/dev/null

# 清理包管理器缓存
echo "Cleaning package manager cache..."
sudo apt clean
sudo apt autoremove -y

echo "Resource cleanup completed!"
```

## 监控命令

### 查看系统资源使用情况
```bash
# 实时查看系统资源
htop

# 查看磁盘使用情况
df -h

# 查看内存使用情况
free -h
```

### 查看 Docker 资源使用情况
```bash
# 查看容器资源使用情况
docker stats

# 查看 Docker 磁盘使用情况
docker system df
```

### 查看日志
```bash
# 查看 Nginx 访问日志
tail -f /var/log/nginx/access.log

# 查看 Nginx 错误日志
tail -f /var/log/nginx/error.log

# 查看应用日志
docker-compose logs -f
```

## 易错点及解决方案

### 1. 监控数据不准确
**问题：**
监控指标与实际使用情况不符

**解决方案：**
检查监控工具配置，确保采集间隔和指标定义正确

### 2. 日志文件过大
**问题：**
日志文件占用过多磁盘空间

**解决方案：**
配置日志轮转，定期清理旧日志

### 3. 告警误报
**问题：**
频繁收到误报信息

**解决方案：**
调整告警阈值，增加告警确认机制

### 4. 性能优化效果不明显
**问题：**
优化后性能提升有限

**解决方案：**
使用性能分析工具定位瓶颈，针对性优化

## 今日任务检查清单
- [ ] 配置性能监控
- [ ] 实施日志管理策略
- [ ] 设置健康检查和告警
- [ ] 优化 Nginx 配置
- [ ] 配置日志轮转
- [ ] 测试监控系统

## 扩展阅读
- [Prometheus 监控系统](https://prometheus.io/docs/introduction/overview/)
- [Grafana 仪表板](https://grafana.com/docs/grafana/latest/)
- [Linux 系统监控](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system_administrators_guide/chap-monitoring_and_automation)
- [Docker 监控最佳实践](https://docs.docker.com/config/containers/resource_constraints/)