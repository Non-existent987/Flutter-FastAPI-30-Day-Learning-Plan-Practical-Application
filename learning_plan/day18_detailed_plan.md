# Day 18 详细学习计划：用户体验优化（加载与错误处理）

## 学习目标
- 实现更精细的加载状态管理
- 完善错误处理机制
- 添加网络状态监听
- 优化用户交互反馈

## 知识点详解

### 1. 加载状态管理
**粒度控制：**
- 全局加载状态
- 局部加载状态
- 按钮加载状态

**视觉反馈：**
- 骨架屏
- 进度条
- 加载文本

### 2. 错误处理机制
**错误分类：**
- 网络错误
- 服务端错误
- 客户端错误
- 未知错误

**处理策略：**
- 重试机制
- 错误降级
- 用户引导

### 3. 网络状态监听
**功能：**
- 网络连接状态检测
- 网络类型识别
- 离线数据处理

## 练习代码

### 1. 创建网络状态监听服务

#### 创建 services/connectivity_service.dart
```dart
import 'dart:async';
import 'package:connectivity_plus/connectivity_plus.dart';

class ConnectivityService {
  static final ConnectivityService _instance = ConnectivityService._internal();
  factory ConnectivityService() => _instance;
  ConnectivityService._internal();

  final Connectivity _connectivity = Connectivity();
  final StreamController<ConnectivityResult> _controller = 
      StreamController<ConnectivityResult>.broadcast();

  Stream<ConnectivityResult> get onConnectivityChanged => _controller.stream;

  bool _hasConnection = false;
  bool get hasConnection => _hasConnection;

  Future<void> init() async {
    // 获取初始连接状态
    final result = await _connectivity.checkConnectivity();
    _hasConnection = _isConnected(result);
    _controller.add(result);
    
    // 监听连接状态变化
    _connectivity.onConnectivityChanged.listen((result) {
      _hasConnection = _isConnected(result);
      _controller.add(result);
    });
  }

  bool _isConnected(ConnectivityResult result) {
    return result != ConnectivityResult.none;
  }

  Future<bool> isConnected() async {
    final result = await _connectivity.checkConnectivity();
    return _isConnected(result);
  }

  void dispose() {
    _controller.close();
  }
}
```

### 2. 创建网络感知的基组件

#### 创建 components/network_aware_widget.dart
```dart
import 'package:flutter/material.dart';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'services/connectivity_service.dart';

class NetworkAwareWidget extends StatefulWidget {
  final Widget Function(bool isConnected) builder;
  final Widget? disconnectedWidget;

  const NetworkAwareWidget({
    Key? key,
    required this.builder,
    this.disconnectedWidget,
  }) : super(key: key);

  @override
  State<NetworkAwareWidget> createState() => _NetworkAwareWidgetState();
}

class _NetworkAwareWidgetState extends State<NetworkAwareWidget> {
  late StreamSubscription<ConnectivityResult> _subscription;
  bool _isConnected = true;

  @override
  void initState() {
    super.initState();
    _checkInitialConnectivity();
    _subscribeToConnectivityChanges();
  }

  Future<void> _checkInitialConnectivity() async {
    _isConnected = await ConnectivityService().isConnected();
    if (mounted) {
      setState(() {});
    }
  }

  void _subscribeToConnectivityChanges() {
    _subscription = ConnectivityService().onConnectivityChanged.listen((result) {
      if (mounted) {
        setState(() {
          _isConnected = result != ConnectivityResult.none;
        });
      }
    });
  }

  @override
  void dispose() {
    _subscription.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (!_isConnected) {
      return widget.disconnectedWidget ??
          Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(
                  Icons.wifi_off,
                  size: 48,
                  color: Colors.grey,
                ),
                const SizedBox(height: 16),
                const Text(
                  '网络连接不可用',
                  style: TextStyle(fontSize: 18),
                ),
                const SizedBox(height: 8),
                const Text(
                  '请检查您的网络设置',
                  style: TextStyle(color: Colors.grey),
                ),
                const SizedBox(height: 24),
                ElevatedButton.icon(
                  onPressed: _checkInitialConnectivity,
                  icon: const Icon(Icons.refresh),
                  label: const Text('重试'),
                ),
              ],
            ),
          );
    }

    return widget.builder(_isConnected);
  }
}
```

### 3. 创建带重试功能的 FutureBuilder

#### 创建 components/retry_future_builder.dart
```dart
import 'package:flutter/material.dart';

class RetryFutureBuilder<T> extends StatefulWidget {
  final Future<T>? future;
  final AsyncWidgetBuilder<T> builder;
  final VoidCallback? onRetry;
  final Widget? retryButton;
  final Duration? retryDelay;

  const RetryFutureBuilder({
    Key? key,
    required this.future,
    required this.builder,
    this.onRetry,
    this.retryButton,
    this.retryDelay,
  }) : super(key: key);

  @override
  State<RetryFutureBuilder<T>> createState() => _RetryFutureBuilderState<T>();
}

class _RetryFutureBuilderState<T> extends State<RetryFutureBuilder<T>> {
  late Future<T>? _future;

  @override
  void initState() {
    super.initState();
    _future = widget.future;
  }

  @override
  void didUpdateWidget(covariant RetryFutureBuilder<T> oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.future != widget.future) {
      _future = widget.future;
    }
  }

  void _retry() {
    if (widget.onRetry != null) {
      widget.onRetry!();
    }
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<T>(
      future: _future,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return widget.builder(context, snapshot);
        } else if (snapshot.hasError) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(
                  Icons.error_outline,
                  size: 48,
                  color: Colors.red,
                ),
                const SizedBox(height: 16),
                Text(
                  '加载失败: ${snapshot.error}',
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 16),
                widget.retryButton ??
                    ElevatedButton.icon(
                      onPressed: _retry,
                      icon: const Icon(Icons.refresh),
                      label: const Text('重试'),
                    ),
              ],
            ),
          );
        } else {
          return widget.builder(context, snapshot);
        }
      },
    );
  }
}
```

### 4. 更新主页以使用网络感知组件

#### 更新 screens/home_screen.dart
```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:my_tutorial_site/components/article_card.dart';
import 'package:my_tutorial_site/components/skeleton_loader.dart';
import 'package:my_tutorial_site/components/fade_animation.dart';
import 'package:my_tutorial_site/components/network_aware_widget.dart';
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
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();

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
      key: _scaffoldKey,
      appBar: AppBar(
        title: const Text('Flutter + FastAPI 教程网站'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadArticles,
            tooltip: '刷新',
          ),
          IconButton(
            icon: const Icon(Icons.brightness_6),
            onPressed: () {
              // TODO: 切换主题
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('主题切换功能待实现')),
              );
            },
            tooltip: '切换主题',
          ),
        ],
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            const DrawerHeader(
              decoration: BoxDecoration(
                color: Color(0xFF2196F3),
              ),
              child: Text(
                '课程目录',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                ),
              ),
            ),
            ListTile(
              leading: const Icon(Icons.home),
              title: const Text('首页'),
              onTap: () {
                Navigator.pop(context);
              },
            ),
            const Divider(),
            ListTile(
              leading: const Icon(Icons.book),
              title: const Text('第1周：后端基础'),
              onTap: () {
                Navigator.pop(context);
              },
            ),
            ListTile(
              leading: const Icon(Icons.book),
              title: const Text('第2周：前端基础'),
              onTap: () {
                Navigator.pop(context);
              },
            ),
            ListTile(
              leading: const Icon(Icons.book),
              title: const Text('第3周：全栈整合'),
              onTap: () {
                Navigator.pop(context);
              },
            ),
            ListTile(
              leading: const Icon(Icons.book),
              title: const Text('第4周：部署上线'),
              onTap: () {
                Navigator.pop(context);
              },
            ),
          ],
        ),
      ),
      body: Row(
        children: [
          // 左侧导航栏（大屏幕显示）
          MediaQuery.of(context).size.width > 800
              ? Expanded(
                  flex: 1,
                  child: Container(
                    color: Theme.of(context).brightness == Brightness.light
                        ? Colors.grey[300]
                        : Colors.grey[800],
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
                )
              : const SizedBox.shrink(),
          
          // 右侧内容区域
          Expanded(
            flex: MediaQuery.of(context).size.width > 800 ? 3 : 1,
            child: Container(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      if (MediaQuery.of(context).size.width <= 800)
                        IconButton(
                          icon: const Icon(Icons.menu),
                          onPressed: () {
                            _scaffoldKey.currentState?.openDrawer();
                          },
                        ),
                      const SizedBox(width: 8),
                      const Text(
                        '最新教程',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Expanded(
                    child: NetworkAwareWidget(
                      builder: (isConnected) {
                        return RefreshIndicator(
                          onRefresh: () async {
                            if (isConnected) {
                              _loadArticles();
                              // 等待 Future 完成
                              await _articlesFuture;
                            }
                          },
                          child: FutureBuilder<List<Article>>(
                            future: _articlesFuture,
                            builder: (context, snapshot) {
                              if (snapshot.connectionState == ConnectionState.waiting) {
                                return const SkeletonLoader();
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
                                    return FadeAnimation(
                                      delay: Duration(milliseconds: 100 * index),
                                      child: ArticleCard(
                                        title: article.title,
                                        summary: _getSummaryFromMarkdown(article.content),
                                        author: article.author,
                                        isPublished: article.published,
                                        onTap: () {
                                          // 使用 go_router 导航到文章详情页
                                          context.push('/article/${article.id}', extra: article);
                                        },
                                      ),
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
                        );
                      },
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

### 5. 添加 connectivity_plus 依赖

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
  go_router: ^6.0.1
  connectivity_plus: ^3.0.2  # 添加网络连接状态检测包

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

### 6. 更新主应用初始化网络服务

#### 更新 lib/main.dart
```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'components/error_boundary.dart';
import 'router/app_router.dart';
import 'themes/app_theme.dart';
import 'services/connectivity_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // 初始化网络连接服务
  await ConnectivityService().init();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Tutorial Site',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system, // 跟随系统主题
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
                    Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: Theme.of(context).errorColor.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        '错误信息: $error',
                        style: const TextStyle(fontFamily: 'monospace'),
                      ),
                    ),
                    const SizedBox(height: 16),
                    ElevatedButton.icon(
                      onPressed: () {
                        // 重启应用
                        context.go('/');
                      },
                      icon: const Icon(Icons.refresh),
                      label: const Text('返回首页'),
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

### 7. 更新项目结构
```
lib/
├── main.dart
├── components/
│   ├── article_card.dart
│   ├── error_boundary.dart
│   ├── error_display.dart
│   ├── fade_animation.dart
│   ├── loading_indicator.dart
│   ├── markdown_viewer.dart
│   ├── network_aware_widget.dart
│   ├── retry_future_builder.dart
│   └── skeleton_loader.dart
├── models/
│   └── article.dart
├── router/
│   └── app_router.dart
├── services/
│   ├── api_service.dart
│   └── connectivity_service.dart
├── screens/
│   ├── article_detail_screen.dart
│   └── home_screen.dart
├── themes/
│   └── app_theme.dart
```

## 易错点及解决方案

### 1. 网络状态监听不准确
**问题：**
网络状态变化未能及时反映到UI

**解决方案：**
使用 Stream 方式监听网络变化，确保UI及时更新

### 2. 重试机制无限循环
**问题：**
在网络持续不可用时，重试操作形成无限循环

**解决方案：**
添加重试次数限制或延迟重试机制

### 3. 内存泄漏
**问题：**
StreamSubscription 未正确释放导致内存泄漏

**解决方案：**
在组件 dispose 时取消订阅

### 4. 离线状态下用户操作处理
**问题：**
用户在离线状态下执行需要网络的操作时没有适当反馈

**解决方案：**
提前检查网络状态，给出相应提示

## 今日任务检查清单
- [ ] 添加 connectivity_plus 依赖
- [ ] 创建网络状态监听服务
- [ ] 实现网络感知组件
- [ ] 更新主页以支持网络状态检测
- [ ] 测试各种网络状况下的应用表现

## 扩展阅读
- [Flutter 网络连接状态检测](https://pub.dev/packages/connectivity_plus)
- [错误处理最佳实践](https://flutter.dev/docs/testing/errors)
- [用户体验设计](https://uxdesign.cc/)