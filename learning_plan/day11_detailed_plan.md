# Day 11 详细学习计划：网络请求与异步编程

## 学习目标
- 学习 Flutter 网络请求
- 理解 Future 和 async/await
- 实现与后端 API 的数据交互
- 处理 HTTP 响应

## 知识点详解

### 1. HTTP 客户端选择
**http 包：**
- 官方推荐的轻量级 HTTP 客户端
- 简单易用
- 支持常见的 HTTP 方法

**dio 包：**
- 功能更丰富的 HTTP 客户端
- 支持拦截器、全局配置等高级功能
- 更适合复杂项目

### 2. 异步编程概念
**Future：**
- 表示异步操作的结果
- 可以通过 then/catchError 处理结果

**async/await：**
- 更直观的异步编程语法
- 使异步代码看起来像同步代码

### 3. JSON 序列化
**手动序列化：**
- 简单直接
- 适用于小项目

**json_serializable：**
- 自动生成序列化代码
- 类型安全
- 适用于大项目

## 练习代码

### 1. 添加依赖

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
  http: ^0.13.5  # 添加 http 包

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

### 2. 数据模型定义

#### 创建 models/article.dart
```dart
class Article {
  final int id;
  final String title;
  final String content;
  final String? author;
  final bool published;
  final DateTime? createdAt;

  Article({
    required this.id,
    required this.title,
    required this.content,
    this.author,
    required this.published,
    this.createdAt,
  });

  // 从 JSON 创建 Article 对象
  factory Article.fromJson(Map<String, dynamic> json) {
    return Article(
      id: json['id'],
      title: json['title'],
      content: json['content'],
      author: json['author'],
      published: json['published'] ?? false,
      createdAt: json['created_at'] != null
          ? DateTime.parse(json['created_at'])
          : null,
    );
  }

  // 将 Article 对象转换为 JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'content': content,
      'author': author,
      'published': published,
      'created_at': createdAt?.toIso8601String(),
    };
  }
}
```

### 3. 网络请求服务

#### 创建 services/api_service.dart
```dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/article.dart';

class ApiService {
  // 后端 API 地址
  static const String baseUrl = 'http://localhost:8000';
  static const String articlesEndpoint = '/articles/';

  // 获取文章列表
  static Future<List<Article>> fetchArticles() async {
    final response = await http.get(Uri.parse('$baseUrl$articlesEndpoint'));

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
    final response = await http.get(
      Uri.parse('$baseUrl$articlesEndpoint$id'),
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
    final response = await http.post(
      Uri.parse('$baseUrl$articlesEndpoint'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(article.toJson()),
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

### 4. 在界面中使用网络请求

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
  List<Article> articles = [];
  bool isLoading = false;
  String errorMessage = '';

  @override
  void initState() {
    super.initState();
    _loadArticles();
  }

  // 加载文章列表
  Future<void> _loadArticles() async {
    setState(() {
      isLoading = true;
      errorMessage = '';
    });

    try {
      final fetchedArticles = await ApiService.fetchArticles();
      setState(() {
        articles = fetchedArticles;
      });
    } catch (error) {
      setState(() {
        errorMessage = '加载文章失败: $error';
      });
    } finally {
      setState(() {
        isLoading = false;
      });
    }
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
                  if (isLoading)
                    const Center(child: CircularProgressIndicator())
                  else if (errorMessage.isNotEmpty)
                    Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(errorMessage),
                          const SizedBox(height: 16),
                          ElevatedButton(
                            onPressed: _loadArticles,
                            child: const Text('重试'),
                          ),
                        ],
                      ),
                    )
                  else
                    Expanded(
                      child: RefreshIndicator(
                        onRefresh: _loadArticles,
                        child: ListView.builder(
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
                                // 点击文章卡片的处理
                                ScaffoldMessenger.of(context).showSnackBar(
                                  SnackBar(
                                    content: Text('打开文章: ${article.title}'),
                                  ),
                                );
                              },
                            );
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

### 5. 项目结构更新
```
lib/
├── main.dart
├── components/
│   └── article_card.dart
├── models/
│   └── article.dart
├── services/
│   └── api_service.dart
```

## 易错点及解决方案

### 1. 跨域问题
**问题：**
浏览器控制台报跨域错误

**解决方案：**
确保后端已正确配置 CORS：
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. 网络请求阻塞 UI
**问题：**
网络请求导致界面卡顿

**解决方案：**
使用 async/await 和 Future 正确处理异步操作

### 3. JSON 解析错误
**问题：**
字段类型不匹配或字段缺失

**解决方案：**
添加空值检查和类型转换：
```dart
factory Article.fromJson(Map<String, dynamic> json) {
  return Article(
    id: json['id'] as int,
    title: json['title'] as String,
    content: json['content'] as String,
    author: json['author'] as String?,
    published: json['published'] as bool? ?? false,
  );
}
```

### 4. 状态管理混乱
**问题：**
网络请求状态更新不及时

**解决方案：**
使用 setState 正确更新组件状态，合理处理加载、成功、失败三种状态

## 今日任务检查清单
- [ ] 添加 http 包依赖
- [ ] 创建 Article 数据模型
- [ ] 实现 ApiService 网络请求服务
- [ ] 在界面中加载并显示文章列表
- [ ] 处理网络请求的各种状态（加载中、成功、失败）

## 扩展阅读
- [Flutter HTTP 请求](https://flutter.dev/docs/cookbook/networking/send-data)
- [Dart 异步编程](https://dart.dev/codelabs/async-await)
- [JSON 和序列化](https://flutter.dev/docs/development/data-and-backend/json)