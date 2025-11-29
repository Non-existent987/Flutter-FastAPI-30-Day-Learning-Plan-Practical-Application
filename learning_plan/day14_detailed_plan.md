# Day 14 详细学习计划：前端攻坚与功能完善

## 学习目标
- 完善前端功能
- 优化用户体验
- 实现错误边界处理
- 完成前端 MVP 版本

## 知识点详解

### 1. 错误边界处理
**概念：**
- 捕获并处理子组件树中的 JavaScript 异常
- 防止整个应用崩溃
- 提供降级 UI

### 2. 用户体验优化
**要点：**
- 加载状态提示
- 错误信息友好化
- 交互反馈及时
- 界面响应迅速

### 3. 应用状态管理
**简单状态管理：**
- 使用 StatefulWidget 管理局部状态
- 通过回调函数传递状态变化
- 适用于小型应用

## 练习代码

### 1. 创建错误边界组件

#### 创建 components/error_boundary.dart
```dart
import 'package:flutter/material.dart';

class ErrorBoundary extends StatefulWidget {
  final Widget child;
  final Widget Function(Object error, StackTrace stack)? errorBuilder;

  const ErrorBoundary({
    Key? key,
    required this.child,
    this.errorBuilder,
  }) : super(key: key);

  @override
  State<ErrorBoundary> createState() => _ErrorBoundaryState();
}

class _ErrorBoundaryState extends State<ErrorBoundary> {
  Object? _error;
  StackTrace? _stack;

  @override
  Widget build(BuildContext context) {
    if (_error != null) {
      if (widget.errorBuilder != null) {
        return widget.errorBuilder!(_error!, _stack!);
      }

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
              Text('错误信息: $_error'),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: () {
                  setState(() {
                    _error = null;
                    _stack = null;
                  });
                },
                child: const Text('重试'),
              ),
            ],
          ),
        ),
      );
    }

    return _ErrorBoundaryWrapper(
      onError: (error, stack) {
        setState(() {
          _error = error;
          _stack = stack;
        });
      },
      child: widget.child,
    );
  }
}

class _ErrorBoundaryWrapper extends StatefulWidget {
  final Widget child;
  final Function(Object error, StackTrace stack) onError;

  const _ErrorBoundaryWrapper({
    Key? key,
    required this.child,
    required this.onError,
  }) : super(key: key);

  @override
  State<_ErrorBoundaryWrapper> createState() => _ErrorBoundaryWrapperState();
}

class _ErrorBoundaryWrapperState extends State<_ErrorBoundaryWrapper> {
  @override
  Widget build(BuildContext context) {
    return widget.child;
  }

  @override
  void reassemble() {
    // 开发环境下重新构建时捕获错误
    try {
      super.reassemble();
    } catch (error, stack) {
      widget.onError(error, stack);
    }
  }

  @override
  void didChangeDependencies() {
    try {
      super.didChangeDependencies();
    } catch (error, stack) {
      widget.onError(error, stack);
    }
  }
}
```

### 2. 创建加载指示器组件

#### 创建 components/loading_indicator.dart
```dart
import 'package:flutter/material.dart';

class LoadingIndicator extends StatelessWidget {
  final String message;

  const LoadingIndicator({Key? key, this.message = '加载中...'}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const CircularProgressIndicator(),
          const SizedBox(height: 16),
          Text(message),
        ],
      ),
    );
  }
}
```

### 3. 创建错误显示组件

#### 创建 components/error_display.dart
```dart
import 'package:flutter/material.dart';

class ErrorDisplay extends StatelessWidget {
  final String message;
  final VoidCallback? onRetry;

  const ErrorDisplay({
    Key? key,
    required this.message,
    this.onRetry,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
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
            message,
            textAlign: TextAlign.center,
            style: const TextStyle(fontSize: 16),
          ),
          const SizedBox(height: 16),
          if (onRetry != null)
            ElevatedButton(
              onPressed: onRetry,
              child: const Text('重试'),
            ),
        ],
      ),
    );
  }
}
```

### 4. 更新主应用结构

#### 更新 lib/main.dart
```dart
import 'package:flutter/material.dart';
import 'components/error_boundary.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Tutorial Site',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatelessWidget {
  const MyHomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
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
                    Navigator.pushAndRemoveUntil(
                      context,
                      MaterialPageRoute(builder: (context) => const MyHomePage()),
                      (route) => false,
                    );
                  },
                  child: const Text('重启应用'),
                ),
              ],
            ),
          ),
        );
      },
      child: const HomeScreen(),
    );
  }
}
```

### 5. 创建主页屏幕

#### 创建 screens/home_screen.dart
```dart
import 'package:flutter/material.dart';
import 'package:my_tutorial_site/components/article_card.dart';
import 'package:my_tutorial_site/models/article.dart';
import 'package:my_tutorial_site/services/api_service.dart';
import 'package:my_tutorial_site/screens/article_detail_screen.dart';
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
                                    // 导航到文章详情页
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (context) => ArticleDetailPage(
                                          article: article,
                                        ),
                                      ),
                                    );
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

### 6. 更新项目结构
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
├── services/
│   └── api_service.dart
├── screens/
│   ├── article_detail_screen.dart
│   └── home_screen.dart
```

## 易错点及解决方案

### 1. 错误边界无法捕获所有错误
**问题：**
某些异步错误或构建错误无法被捕获

**解决方案：**
结合 try/catch 和 Future.catchError 使用，确保关键异步操作有错误处理

### 2. 下拉刷新状态不同步
**问题：**
RefreshIndicator 与 FutureBuilder 状态不同步

**解决方案：**
在 onRefresh 中等待 Future 完成，确保状态一致

### 3. 组件复用性差
**问题：**
组件与业务逻辑耦合过紧

**解决方案：**
通过参数化提高组件通用性，分离业务逻辑和UI逻辑

### 4. 错误信息不友好
**问题：**
直接显示技术性错误信息给用户

**解决方案：**
对错误信息进行分类和转换，显示用户友好的提示

## 今日任务检查清单
- [ ] 实现错误边界处理
- [ ] 创建通用加载和错误组件
- [ ] 完善主页 UI 和功能
- [ ] 优化用户体验
- [ ] 完成前端 MVP 版本

## 扩展阅读
- [Flutter 错误处理](https://flutter.dev/docs/testing/errors)
- [用户体验设计原则](https://uxdesign.cc/)
- [Material Design 指南](https://material.io/design)