# Day 22 详细学习计划：Flutter Web 应用构建

## 学习目标
- 学习 Flutter Web 构建流程
- 创建生产环境构建配置
- 优化构建产物
- 理解静态资源部署

## 知识点详解

### 1. Flutter Web 构建基础
**构建命令：**
- `flutter build web`：构建生产版本
- `flutter build web --release`：构建发布版本
- `flutter build web --profile`：构建性能分析版本

**构建产物：**
- HTML 文件
- JavaScript 文件
- CSS 样式文件
- 资源文件（图片、字体等）

### 2. 构建优化
**代码分割：**
- 减小初始加载体积
- 按需加载模块
- 提高首屏渲染速度

**资源优化：**
- 图片压缩
- 字体子集化
- 资源缓存策略

### 3. 环境配置
**不同环境配置：**
- 开发环境
- 测试环境
- 生产环境

**配置管理：**
- 环境变量
- 配置文件
- 编译时变量

## 练习代码

### 1. 创建构建配置文件

#### 创建 web/manifest.json
```json
{
    "name": "Flutter Fast Tutorial Site",
    "short_name": "Tutorial Site",
    "start_url": ".",
    "display": "standalone",
    "background_color": "#0175C2",
    "theme_color": "#0175C2",
    "description": "A tutorial site built with Flutter and FastAPI.",
    "orientation": "portrait-primary",
    "prefer_related_applications": false,
    "icons": [
        {
            "src": "icons/Icon-192.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "icons/Icon-512.png",
            "sizes": "512x512",
            "type": "image/png"
        },
        {
            "src": "icons/Icon-maskable-192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "maskable"
        },
        {
            "src": "icons/Icon-maskable-512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "maskable"
        }
    ]
}
```

### 2. 更新 index.html 文件

#### 更新 web/index.html
```html
<!DOCTYPE html>
<html>
<head>
    <!--
    If you are serving your web app in a path other than the root, change the
    href value below to reflect the base path you are serving from.

    The path provided below has to start and end with a slash "/" in order for
    it to work correctly.

    For more details:
    * https://developer.mozilla.org/en-US/docs/Web/HTML/Element/base

    This is a placeholder for base href that will be replaced by the value of
    the `--base-href` argument provided to `flutter build`.
  -->
    <base href="$FLUTTER_BASE_HREF">

    <meta charset="UTF-8">
    <meta content="IE=Edge" http-equiv="X-UA-Compatible">
    <meta name="description" content="A tutorial site built with Flutter and FastAPI for learning full-stack development in 30 days.">

    <!-- iOS meta tags & icons -->
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="apple-mobile-web-app-title" content="Tutorial Site">
    <link rel="apple-touch-icon" href="icons/Icon-192.png">

    <!-- Favicon -->
    <link rel="icon" type="image/png" href="favicon.png"/>

    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="Flutter + FastAPI 30天速成">
    <meta property="og:description" content="边学边做的全栈实践计划，掌握Flutter和FastAPI开发技能">
    <meta property="og:image" content="icons/Icon-512.png">
    <meta property="og:url" content="https://yourdomain.com">
    <meta property="og:type" content="website">

    <title>Flutter + FastAPI 教程网站</title>
    <link rel="manifest" href="manifest.json">

    <script>
        // Flutter 脚本加载前的初始化代码
        window.addEventListener('load', function(ev) {
            // 下载主要的 Dart WASM/JS 代码
            _flutter.loader.loadEntrypoint({
                serviceWorker: {
                    serviceWorkerVersion: serviceWorkerVersion,
                },
                onEntrypointLoaded: function(engineInitializer) {
                    engineInitializer.initializeEngine().then(function(appRunner) {
                        appRunner.runApp();
                    });
                }
            });
        });
    </script>
</head>
<body>
    <!-- Flutter 应用加载时显示的占位符 -->
    <div id="loading-placeholder" style="position: fixed; inset: 0; display: flex; justify-content: center; align-items: center; background-color: #f5f5f5;">
        <div style="text-align: center;">
            <div style="width: 48px; height: 48px; border: 4px solid #2196F3; border-top-color: transparent; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto;"></div>
            <p style="margin-top: 16px; font-family: Arial, sans-serif; color: #666;">加载中...</p>
        </div>
    </div>
    
    <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</body>
</html>
```

### 3. 创建环境配置文件

#### 创建 lib/config/environment.dart
```dart
class Environment {
  static const String dev = 'dev';
  static const String staging = 'staging';
  static const String prod = 'prod';
  
  static String get currentEnvironment {
    // 在实际应用中，可以通过编译时常量或环境变量设置
    return const String.fromEnvironment('ENVIRONMENT', defaultValue: 'dev');
  }
  
  static bool get isDev => currentEnvironment == dev;
  static bool get isStaging => currentEnvironment == staging;
  static bool get isProd => currentEnvironment == prod;
}
```

#### 创建 lib/config/api_config.dart
```dart
import 'environment.dart';

class ApiConfig {
  static String get baseUrl {
    switch (Environment.currentEnvironment) {
      case Environment.prod:
        return 'https://yourdomain.com/api'; // 生产环境 API 地址
      case Environment.staging:
        return 'https://staging.yourdomain.com/api'; // 测试环境 API 地址
      case Environment.dev:
      default:
        return 'http://localhost:8000'; // 开发环境 API 地址
    }
  }
  
  static const int connectTimeout = 10000; // 10秒连接超时
  static const int receiveTimeout = 10000; // 10秒接收超时
}
```

### 4. 更新 API 服务以支持环境配置

#### 更新 services/api_service.dart
```dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/article.dart';
import '../config/api_config.dart';

class ApiService {
  static const String articlesEndpoint = '/articles/';

  // 获取文章列表
  static Future<List<Article>> fetchArticles() async {
    final url = Uri.parse('${ApiConfig.baseUrl}$articlesEndpoint');
    final response = await http.get(url).timeout(
      Duration(milliseconds: ApiConfig.connectTimeout),
    );

    if (response.statusCode == 200) {
      // 解析 JSON 数据
      final List<dynamic> jsonData = json.decode(response.body);
      // 转换为 Article 对象列表
      return jsonData.map((data) => Article.fromJson(data)).toList();
    } else {
      // 抛出异常
      throw Exception('获取文章列表失败: ${response.statusCode}');
    }
  }

  // 获取单个文章
  static Future<Article> fetchArticle(int id) async {
    final url = Uri.parse('${ApiConfig.baseUrl}$articlesEndpoint$id');
    final response = await http.get(url).timeout(
      Duration(milliseconds: ApiConfig.connectTimeout),
    );

    if (response.statusCode == 200) {
      final jsonData = json.decode(response.body);
      return Article.fromJson(jsonData);
    } else {
      throw Exception('获取文章失败: ${response.statusCode}');
    }
  }

  // 创建新文章
  static Future<Article> createArticle(Article article) async {
    final url = Uri.parse('${ApiConfig.baseUrl}$articlesEndpoint');
    final response = await http.post(
      url,
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(article.toJson()),
    ).timeout(
      Duration(milliseconds: ApiConfig.connectTimeout),
    );

    if (response.statusCode == 201) {
      final jsonData = json.decode(response.body);
      return Article.fromJson(jsonData);
    } else {
      throw Exception('创建文章失败: ${response.statusCode}');
    }
  }
}
```

### 5. 创建构建脚本

#### 创建 scripts/build_flutter_web.sh (Linux/Mac)
```bash
#!/bin/bash

echo "Building Flutter Web Application..."

# 清理之前的构建产物
echo "Cleaning previous builds..."
flutter clean
flutter pub get

# 构建 Web 应用
echo "Building release version..."
flutter build web \
  --release \
  --dart-define=ENVIRONMENT=prod \
  --base-href=/ \
  --web-renderer canvaskit

echo "Build completed!"
echo "Output directory: build/web"

# 显示构建产物大小
echo "Build output size:"
du -sh build/web

# 列出主要文件
echo "Main output files:"
ls -lh build/web | head -10
```

#### 创建 scripts/build_flutter_web.bat (Windows)
```batch
@echo off

echo Building Flutter Web Application...

REM 清理之前的构建产物
echo Cleaning previous builds...
flutter clean
flutter pub get

REM 构建 Web 应用
echo Building release version...
flutter build web ^
  --release ^
  --dart-define=ENVIRONMENT=prod ^
  --base-href=/ ^
  --web-renderer canvaskit

echo Build completed!
echo Output directory: build/web

REM 显示构建产物大小
echo Build output size:
powershell "Get-ChildItem -Recurse build/web | Measure-Object -Property Length -Sum"

echo Main output files:
dir build\web /B

pause
```

### 6. 创建优化构建脚本

#### 创建 scripts/build_optimized.sh (Linux/Mac)
```bash
#!/bin/bash

echo "Building optimized Flutter Web Application..."

# 清理和获取依赖
flutter clean
flutter pub get

# 构建优化版本
flutter build web \
  --release \
  --dart-define=ENVIRONMENT=prod \
  --base-href=/ \
  --web-renderer canvaskit \
  --no-source-maps \
  --tree-shake-icons \
  --dart2js-optimization -O4

echo "Optimized build completed!"

# 分析构建产物
echo "Analyzing build output..."
ls -lah build/web

# 检查主要文件大小
echo "Main file sizes:"
echo "main.dart.js:" $(du -h build/web/main.dart.js | cut -f1)
echo "index.html:" $(du -h build/web/index.html | cut -f1)
echo "assets dir:" $(du -h build/web/assets | cut -f1)
```

### 7. 创建部署准备脚本

#### 创建 scripts/prepare_deployment.sh (Linux/Mac)
```bash
#!/bin/bash

echo "Preparing deployment package..."

# 构建应用
./scripts/build_flutter_web.sh

# 创建部署目录
DEPLOY_DIR="deployment/$(date +%Y%m%d_%H%M%S)"
mkdir -p $DEPLOY_DIR

# 复制构建产物
cp -r build/web/* $DEPLOY_DIR/

# 创建部署说明
cat > $DEPLOY_DIR/DEPLOYMENT.md << EOF
# 部署说明

## 部署时间
$(date)

## 部署内容
- Flutter Web 应用静态文件

## 部署步骤
1. 将此目录中的所有文件复制到 Web 服务器的静态文件目录
2. 配置 Web 服务器以正确处理静态文件和 API 代理
3. 重启 Web 服务器

## 注意事项
- 确保 Web 服务器已配置 CORS 头部
- 确保 API 服务正常运行
EOF

echo "Deployment package created at: $DEPLOY_DIR"
```

### 8. 创建分析脚本

#### 创建 scripts/analyze_build.sh (Linux/Mac)
```bash
#!/bin/bash

echo "Analyzing Flutter Web build..."

# 检查构建产物大小
echo "=== Build Size Analysis ==="
echo "Total size:"
du -sh build/web

echo "Largest files:"
find build/web -type f -exec du -h {} + | sort -rh | head -10

# 检查关键文件
echo "=== Key Files ==="
MAIN_JS_SIZE=$(du -h build/web/main.dart.js | cut -f1)
INDEX_HTML_SIZE=$(du -h build/web/index.html | cut -f1)

echo "main.dart.js: $MAIN_JS_SIZE"
echo "index.html: $INDEX_HTML_SIZE"

# 提供优化建议
echo "=== Optimization Suggestions ==="
MAIN_JS_KB=$(du -k build/web/main.dart.js | cut -f1)
if [ $MAIN_JS_KB -gt 2000 ]; then
    echo "⚠️  main.dart.js is quite large (${MAIN_JS_KB}KB). Consider:"
    echo "  - Code splitting"
    echo "  - Removing unused packages"
    echo "  - Using --dart2js-optimization -O4 flag"
else
    echo "✅ main.dart.js size is reasonable (${MAIN_JS_KB}KB)"
fi
```

## Flutter Web 构建命令详解

### 基本构建命令
```bash
# 基本构建
flutter build web

# 指定环境变量
flutter build web --dart-define=ENVIRONMENT=prod

# 指定基础路径
flutter build web --base-href=/tutorial/

# 使用 CanvasKit 渲染器（更好性能，更大体积）
flutter build web --web-renderer canvaskit

# 使用 HTML 渲染器（较小体积，性能较低）
flutter build web --web-renderer html
```

### 优化构建命令
```bash
# 完整优化构建
flutter build web \
  --release \
  --dart-define=ENVIRONMENT=prod \
  --web-renderer canvaskit \
  --no-source-maps \
  --tree-shake-icons \
  --dart2js-optimization -O4
```

## 易错点及解决方案

### 1. 构建产物过大
**问题：**
main.dart.js 文件太大影响加载速度

**解决方案：**
```bash
# 启用代码优化
flutter build web --dart2js-optimization -O4

# 启用树摇晃
flutter build web --tree-shake-icons

# 移除 source maps
flutter build web --no-source-maps
```

### 2. API 地址配置错误
**问题：**
生产环境仍使用本地 API 地址

**解决方案：**
使用环境变量配置不同环境的 API 地址

### 3. 路径问题
**问题：**
部署到子路径时资源加载失败

**解决方案：**
正确设置 --base-href 参数

### 4. 渲染性能问题
**问题：**
在某些设备上渲染性能不佳

**解决方案：**
根据目标设备选择合适的渲染器

## 今日任务检查清单
- [ ] 创建 Flutter Web 构建配置
- [ ] 实现环境配置管理
- [ ] 更新 API 服务支持环境配置
- [ ] 创建构建和优化脚本
- [ ] 测试构建产物功能

## 扩展阅读
- [Flutter Web 文档](https://flutter.dev/web)
- [Flutter 构建发布](https://flutter.dev/docs/deployment)
- [Web 渲染器比较](https://flutter.dev/docs/development/tools/web-renderers)