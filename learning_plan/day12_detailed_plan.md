# Day 12 详细学习计划：数据渲染与 FutureBuilder

## 学习目标
- 学习 FutureBuilder 的使用
- 掌握异步数据渲染技巧
- 优化 UI 状态管理
- 实现下拉刷新和错误处理

## 知识点详解

### 1. FutureBuilder 组件
**概念：**
- 专门用于处理异步数据的 Widget
- 根据 Future 的状态显示不同内容
- 简化异步数据的 UI 处理

**状态：**
- ConnectionState.none: Future 为空
- ConnectionState.waiting: Future 正在执行
- ConnectionState.active: Future 有数据流
- ConnectionState.done: Future 执行完毕

### 2. 异步数据渲染优化
**要点：**
- 合理使用加载指示器
- 提供良好的错误反馈
- 实现重试机制
- 添加空状态处理

### 3. 下拉刷新实现
**组件：**
- RefreshIndicator: Material Design 下拉刷新组件
- CupertinoSliverRefreshControl: iOS 风格下拉刷新

## 练习代码

### 1. 使用 FutureBuilder 优化数据渲染

#### 更新 lib/main.dart
```dart
import 'package:flutter/material.dart';
import 'components/article_card.dart';
import 'models/article.dart';
import 'services/api_service.dart';

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
      home: const TutorialHomePage(),
    );
  }
}

class TutorialHomePage extends StatefulWidget {
  const TutorialHomePage({Key? key}) : super(key: key);

  @override
  State<TutorialHomePage> createState() => _TutorialHomePageState();
}

class _TutorialHomePageState extends State<TutorialHomePage> {
  Future<List<Article>>? _articlesFuture;

  @override
  void initState() {
    super.initState();
    _articlesFuture = ApiService.fetchArticles();
  }

  Future<void> _refreshArticles() async {
    setState(() {
      _articlesFuture = ApiService.fetchArticles();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Flutter + FastAPI 教程网站'),
      ),
      body: Row(
        children: [
          // 左侧导航栏
          Expanded(
            flex: 1,
            child: Container(
              color: Colors.grey[300],
              child: ListView(
                children: [
                  ListTile(
                    leading: const Icon(Icons.book),
                    title: const Text('环境搭建'),
                    onTap: () {
                      // TODO: 导航到环境搭建教程
                    },
                  ),
                  ListTile(
                    leading: const Icon(Icons.data_object),
                    title: const Text('数据模型'),
                    onTap: () {
                      // TODO: 导航到数据模型教程
                    },
                  ),
                  ListTile(
                    leading: const Icon(Icons.storage),
                    title: const Text('数据库集成'),
                    onTap: () {
                      // TODO: 导航到数据库集成教程
                    },
                  ),
                  ListTile(
                    leading: const Icon(Icons.api),
                    title: const Text('CRUD 操作'),
                    onTap: () {
                      // TODO: 导航到 CRUD 操作教程
                    },
                  ),
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
                      onRefresh: _refreshArticles,
                      child: FutureBuilder<List<Article>>(
                        future: _articlesFuture,
                        builder: (context, snapshot) {
                          if (snapshot.connectionState == ConnectionState.waiting) {
                            return const Center(
                              child: CircularProgressIndicator(),
                            );
                          } else if (snapshot.hasError) {
                            return Center(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Text('加载失败: ${snapshot.error}'),
                                  const SizedBox(height: 16),
                                  ElevatedButton(
                                    onPressed: _refreshArticles,
                                    child: const Text('重试'),
                                  ),
                                ],
                              ),
                            );
                          } else if (snapshot.hasData) {
                            final articles = snapshot.data!;
                            if (articles.isEmpty) {
                              return const Center(
                                child: Text('暂无文章'),
                              );
                            }
                            return ListView.builder(
                              itemCount: articles.length,
                              itemBuilder: (context, index) {
                                final article = articles[index];
                                return ArticleCard(
                                  title: article.title,
                                  summary: article.content.length > 100
                                      ? '${article.content.substring(0, 100)}...'
                                      : article.content,
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
}
```

### 2. 创建文章详情页面

#### 创建 screens/article_detail_screen.dart
```dart
import 'package:flutter/material.dart';
import '../models/article.dart';

class ArticleDetailPage extends StatelessWidget {
  final Article article;

  const ArticleDetailPage({Key? key, required this.article}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(article.title),
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
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (article.author != null)
              Text(
                '作者: ${article.author}',
                style: const TextStyle(
                  fontSize: 16,
                  color: Colors.blue,
                ),
              ),
            if (article.createdAt != null)
              Text(
                '发布时间: ${article.createdAt.toString().split(' ')[0]}',
                style: const TextStyle(
                  fontSize: 14,
                  color: Colors.grey,
                ),
              ),
            const SizedBox(height: 16),
            const Divider(),
            const SizedBox(height: 16),
            Text(
              article.content,
              style: const TextStyle(fontSize: 16),
            ),
          ],
        ),
      ),
    );
  }
}
```

### 3. 更新 ArticleCard 组件支持导航

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

### 4. 更新项目结构
```
lib/
├── main.dart
├── components/
│   └── article_card.dart
├── models/
│   └── article.dart
├── services/
│   └── api_service.dart
├── screens/
│   └── article_detail_screen.dart
```

## 易错点及解决方案

### 1. FutureBuilder 重建问题
**问题：**
FutureBuilder 在每次重建时都会重新执行 Future

**解决方案：**
将 Future 存储在 State 类的变量中，而不是在 build 方法中创建

### 2. 下拉刷新与 FutureBuilder 冲突
**问题：**
RefreshIndicator 与 FutureBuilder 结合使用时刷新无效

**解决方案：**
在刷新时重新创建 Future 并调用 setState 更新状态

### 3. 空安全处理
**问题：**
可空类型未正确处理导致运行时错误

**解决方案：**
使用 ?. 操作符和 ?? 操作符处理可空值

### 4. 页面导航问题
**问题：**
Navigator.push 后返回数据丢失

**解决方案：**
正确管理页面状态，必要时使用 StatefulWidget

## 今日任务检查清单
- [ ] 使用 FutureBuilder 优化异步数据渲染
- [ ] 实现下拉刷新功能
- [ ] 创建文章详情页面
- [ ] 完善错误处理和空状态处理
- [ ] 实现文章列表到详情页的导航

## 扩展阅读
- [FutureBuilder 官方文档](https://api.flutter.dev/flutter/widgets/FutureBuilder-class.html)
- [异步编程指南](https://dart.dev/codelabs/async-await)
- [页面导航](https://flutter.dev/docs/development/ui/navigation)