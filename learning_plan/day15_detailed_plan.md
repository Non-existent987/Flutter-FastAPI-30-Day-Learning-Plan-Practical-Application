# Day 15 详细学习计划：路由管理与页面导航

## 学习目标
- 学习 go_router 包的使用
- 实现应用路由管理
- 创建多页面导航结构
- 理解路由参数传递

## 知识点详解

### 1. 路由管理的重要性
**好处：**
- 统一管理页面导航
- 支持深层链接
- 提供浏览器历史记录支持
- 简化页面间参数传递

### 2. go_router 简介
**特性：**
- 声明式路由配置
- 支持路由参数
- 支持查询参数
- 支持路由守卫
- 与 Flutter Navigator 2.0 集成

### 3. 路由参数类型
**路径参数：**
- 定义在路径中的参数，如 /article/123

**查询参数：**
- URL 中 ? 后面的参数，如 /article?id=123

**页面间参数传递：**
- 通过路由参数传递数据

## 练习代码

### 1. 添加 go_router 依赖

#### 更新 pubspec.yaml
```yaml
name: my_tutorial_site
description: A new Flutter project.

publish_to: 'none'

version: 1.0.0+1

environment:
  sdk: ">=2.17.0 <3.0.0"

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2
  http: ^0.13.5
  flutter_markdown: ^0.6.14
  url_launcher: ^6.1.7
  go_router: ^6.0.1  # 添加路由管理包

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0

flutter:
  uses-material-design: true
```

运行以下命令安装依赖：
```bash
flutter pub get
```

### 2. 创建路由配置

#### 创建 router/app_router.dart
```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:my_tutorial_site/screens/home_screen.dart';
import 'package:my_tutorial_site/screens/article_detail_screen.dart';
import 'package:my_tutorial_site/models/article.dart';

// 定义路由名称常量
abstract class AppRoutes {
  static const home = 'home';
  static const articleDetail = 'articleDetail';
}

final GoRouter router = GoRouter(
  routes: [
    GoRoute(
      name: AppRoutes.home,
      path: '/',
      builder: (context, state) => const HomeScreen(),
    ),
    GoRoute(
      name: AppRoutes.articleDetail,
      path: '/article/:id',
      builder: (context, state) {
        // 获取路径参数
        final articleId = int.parse(state.pathParameters['id']!);
        
        // 获取额外参数（如果有的话）
        final article = state.extra as Article?;
        
        return ArticleDetailPage(
          articleId: articleId,
          article: article,
        );
      },
    ),
  ],
  
  errorBuilder: (context, state) => Scaffold(
    appBar: AppBar(title: const Text('页面未找到')),
    body: Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Text('抱歉，您访问的页面不存在'),
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: () => context.go('/'),
            child: const Text('返回首页'),
          ),
        ],
      ),
    ),
  ),
);
```

### 3. 更新主应用文件

#### 更新 lib/main.dart
```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'components/error_boundary.dart';
import 'router/app_router.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Tutorial Site',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      routeInformationParser: router.routeInformationParser,
      routerDelegate: router.routerDelegate,
      builder: (context, child) {
        return ErrorBoundary(
          errorBuilder: (error, stack) {
            return Scaffold(
              appBar: AppBar(
                title: const Text('发生错误'),
              ),
              body: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      '应用遇到了一个错误：',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 16),
                    Text('错误信息: $error'),
                    const SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: () {
                        // 重启应用
                        context.go('/');
                      },
                      child: const Text('返回首页'),
                    ),
                  ],
                ),
              ),
            );
          },
          child: child!,
        );
      },
    );
  }
}
```

### 4. 更新文章详情页面以支持路由参数

#### 更新 screens/article_detail_screen.dart
```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../models/article.dart';
import '../services/api_service.dart';
import '../components/markdown_viewer.dart';
import '../components/loading_indicator.dart';
import '../components/error_display.dart';

class ArticleDetailPage extends StatefulWidget {
  final int? articleId;
  final Article? article;

  const ArticleDetailPage({
    Key? key,
    this.articleId,
    this.article,
  }) : super(key: key);

  @override
  State<ArticleDetailPage> createState() => _ArticleDetailPageState();
}

class _ArticleDetailPageState extends State<ArticleDetailPage> {
  Future<Article>? _articleFuture;

  @override
  void initState() {
    super.initState();
    _loadArticle();
  }

  void _loadArticle() {
    if (widget.article != null) {
      // 如果已经提供了文章对象，直接使用
      _articleFuture = Future.value(widget.article);
    } else if (widget.articleId != null) {
      // 否则通过 ID 获取文章
      _articleFuture = ApiService.fetchArticle(widget.articleId!);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: FutureBuilder<Article>(
          future: _articleFuture,
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              return Text(
                snapshot.data!.title,
                style: const TextStyle(fontSize: 16),
              );
            }
            return const Text('文章详情');
          },
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.share),
            onPressed: () {
              // TODO: 实现分享功能
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('分享功能待实现')),
              );
            },
          ),
        ],
      ),
      body: FutureBuilder<Article>(
        future: _articleFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const LoadingIndicator(message: '加载文章中...');
          } else if (snapshot.hasError) {
            return ErrorDisplay(
              message: '加载失败: ${snapshot.error}',
              onRetry: _loadArticle,
            );
          } else if (snapshot.hasData) {
            final article = snapshot.data!;
            return SingleChildScrollView(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // 文章元信息
                    if (article.author != null || article.createdAt != null)
                      Container(
                        padding: const EdgeInsets.only(bottom: 16),
                        child: Row(
                          children: [
                            if (article.author != null)
                              Text(
                                '作者: ${article.author}',
                                style: const TextStyle(
                                  fontSize: 14,
                                  color: Colors.blue,
                                ),
                              ),
                            const Spacer(),
                            if (article.createdAt != null)
                              Text(
                                '发布于: ${_formatDate(article.createdAt!)}',
                                style: const TextStyle(
                                  fontSize: 14,
                                  color: Colors.grey,
                                ),
                              ),
                          ],
                        ),
                      ),

                    // 分割线
                    const Divider(),

                    // Markdown 内容
                    MarkdownViewer(markdownData: article.content),
                  ],
                ),
              ),
            );
          } else {
            return const Center(
              child: Text('未找到文章内容'),
            );
          }
        },
      ),
    );
  }

  // 格式化日期
  String _formatDate(DateTime date) {
    return '${date.year}-${date.month.toString().padLeft(2, '0')}-${date.day.toString().padLeft(2, '0')}';
  }
}
```

### 5. 更新主页以使用新路由

#### 更新 screens/home_screen.dart
```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:my_tutorial_site/components/article_card.dart';
import 'package:my_tutorial_site/models/article.dart';
import 'package:my_tutorial_site/services/api_service.dart';
import 'package:my_tutorial_site/components/loading_indicator.dart';
import 'package:my_tutorial_site/components/error_display.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  Future<List<Article>>? _articlesFuture;

  @override
  void initState() {
    super.initState();
    _loadArticles();
  }

  void _loadArticles() {
    setState(() {
      _articlesFuture = ApiService.fetchArticles();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Flutter + FastAPI 教程网站'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadArticles,
          ),
        ],
      ),
      body: Row(
        children: [
          // 左侧导航栏
          Expanded(
            flex: 1,
            child: Container(
              color: Colors.grey[300],
              child: ListView(
                padding: EdgeInsets.zero,
                children: [
                  _buildNavItem(Icons.home, '首页', true),
                  _buildNavItem(Icons.book, '环境搭建', false),
                  _buildNavItem(Icons.data_object, '数据模型', false),
                  _buildNavItem(Icons.storage, '数据库集成', false),
                  _buildNavItem(Icons.api, 'CRUD 操作', false),
                  _buildNavItem(Icons.markdown, 'Markdown 渲染', false),
                ],
              ),
            ),
          ),
          // 右侧内容区域
          Expanded(
            flex: 3,
            child: Container(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    '最新教程',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 16),
                  Expanded(
                    child: RefreshIndicator(
                      onRefresh: () async {
                        _loadArticles();
                        // 等待 Future 完成
                        await _articlesFuture;
                      },
                      child: FutureBuilder<List<Article>>(
                        future: _articlesFuture,
                        builder: (context, snapshot) {
                          if (snapshot.connectionState == ConnectionState.waiting) {
                            return const LoadingIndicator();
                          } else if (snapshot.hasError) {
                            return ErrorDisplay(
                              message: '加载失败: ${snapshot.error}\n请检查网络连接和后端服务',
                              onRetry: _loadArticles,
                            );
                          } else if (snapshot.hasData) {
                            final articles = snapshot.data!;
                            if (articles.isEmpty) {
                              return const Center(
                                child: Text(
                                  '暂无文章\n点击右上角刷新按钮尝试加载',
                                  textAlign: TextAlign.center,
                                ),
                              );
                            }
                            return ListView.builder(
                              itemCount: articles.length,
                              itemBuilder: (context, index) {
                                final article = articles[index];
                                return ArticleCard(
                                  title: article.title,
                                  summary: _getSummaryFromMarkdown(article.content),
                                  author: article.author,
                                  isPublished: article.published,
                                  onTap: () {
                                    // 使用 go_router 导航到文章详情页
                                    context.push('/article/${article.id}', extra: article);
                                  },
                                );
                              },
                            );
                          } else {
                            return const Center(
                              child: Text('暂无数据'),
                            );
                          }
                        },
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildNavItem(IconData icon, String title, bool isSelected) {
    return ListTile(
      leading: Icon(icon),
      title: Text(title),
      selected: isSelected,
      onTap: () {
        // TODO: 处理导航项点击
      },
    );
  }

  // 从 Markdown 内容中提取摘要
  String _getSummaryFromMarkdown(String content) {
    // 移除 Markdown 标记，简单处理
    String cleanContent = content
        .replaceAll(RegExp(r'!\[.*?\]\(.*?\)'), '') // 移除图片
        .replaceAll(RegExp(r'\[.*?\]\(.*?\)'), '')  // 移除链接
        .replaceAll(RegExp(r'[*#_~`\-+]'), '')      // 移除标记符号
        .replaceAll(RegExp(r'\n\s*\n'), '\n')       // 合并多余空行
        .trim();

    // 返回前100个字符作为摘要
    if (cleanContent.length > 100) {
      return '${cleanContent.substring(0, 100)}...';
    }
    return cleanContent;
  }
}
```

### 6. 更新 ArticleCard 组件注释

#### 更新 components/article_card.dart
```dart
import 'package:flutter/material.dart';

class ArticleCard extends StatelessWidget {
  final String title;
  final String summary;
  final String? author;
  final bool isPublished;
  final VoidCallback onTap;

  const ArticleCard({
    Key? key,
    required this.title,
    required this.summary,
    this.author,
    this.isPublished = false,
    required this.onTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      margin: const EdgeInsets.all(8),
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Expanded(
                    child: Text(
                      title,
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  if (!isPublished)
                    const Chip(
                      label: Text('草稿'),
                      backgroundColor: Colors.orange,
                    ),
                ],
              ),
              const SizedBox(height: 8),
              Text(
                summary,
                style: const TextStyle(
                  fontSize: 14,
                  color: Colors.grey,
                ),
                maxLines: 3,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 8),
              if (author != null)
                Text(
                  '作者: $author',
                  style: const TextStyle(
                    fontSize: 12,
                    color: Colors.blue,
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### 7. 更新项目结构
```
lib/
├── main.dart
├── components/
│   ├── article_card.dart
│   ├── error_boundary.dart
│   ├── error_display.dart
│   ├── loading_indicator.dart
│   └── markdown_viewer.dart
├── models/
│   └── article.dart
├── router/
│   └── app_router.dart
├── services/
│   └── api_service.dart
├── screens/
│   ├── article_detail_screen.dart
│   └── home_screen.dart
```

## 易错点及解决方案

### 1. 路由参数解析错误
**问题：**
路径参数类型转换失败

**解决方案：**
添加错误处理，确保参数类型正确：
```dart
final articleId = int.tryParse(state.pathParameters['id'] ?? '') ?? 0;
```

### 2. 路由守卫未实现
**问题：**
未限制某些页面的访问权限

**解决方案：**
使用 redirect 参数实现路由守卫：
```dart
GoRoute(
  path: '/protected',
  redirect: (context, state) {
    // 检查用户是否已登录
    if (!isLoggedIn) {
      return '/login'; // 重定向到登录页
    }
    return null; // 允许访问
  },
  builder: (context, state) => const ProtectedPage(),
)
```

### 3. 页面状态丢失
**问题：**
导航后页面状态未保存

**解决方案：**
使用 AutomaticKeepAliveClientMixin 保持页面状态：
```dart
class _HomeScreenState extends State<HomeScreen> with AutomaticKeepAliveClientMixin {
  @override
  bool get wantKeepAlive => true;
}
```

### 4. 路由配置复杂
**问题：**
路由配置难以维护

**解决方案：**
将路由拆分为多个文件，按功能模块组织

## 今日任务检查清单
- [ ] 添加 go_router 依赖
- [ ] 创建路由配置文件
- [ ] 实现文章详情页路由
- [ ] 更新主页导航逻辑
- [ ] 测试路由功能

## 扩展阅读
- [go_router 官方文档](https://pub.dev/packages/go_router)
- [Flutter 路由管理](https://flutter.dev/docs/development/ui/navigation)
- [深层链接](https://en.wikipedia.org/wiki/Deep_linking)