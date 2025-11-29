# Day 13 详细学习计划：Markdown 渲染与内容展示

## 学习目标
- 学习 flutter_markdown 包的使用
- 实现 Markdown 内容渲染
- 优化文章详情页展示效果
- 处理 Markdown 样式定制

## 知识点详解

### 1. Markdown 渲染库
**flutter_markdown：**
- Flutter 官方提供的 Markdown 渲染库
- 支持标准 Markdown 语法
- 可自定义样式和标签

### 2. Markdown 语法支持
**支持的语法：**
- 标题 (# H1, ## H2, ### H3...)
- 粗体和斜体 (**bold**, *italic*)
- 列表 (有序和无序)
- 链接和图片
- 代码块和行内代码
- 引用块

### 3. 样式定制
**可定制项：**
- 标题样式
- 链接样式
- 代码块样式
- 列表样式
- 自定义标签处理器

## 练习代码

### 1. 添加 flutter_markdown 依赖

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
  flutter_markdown: ^0.6.14  # 添加 Markdown 渲染包

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

### 2. 创建 Markdown 渲染组件

#### 创建 components/markdown_viewer.dart
```dart
import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:url_launcher/url_launcher.dart';

class MarkdownViewer extends StatelessWidget {
  final String markdownData;

  const MarkdownViewer({Key? key, required this.markdownData}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MarkdownBody(
      data: markdownData,
      selectable: true,
      onTapLink: (text, href, title) {
        // 处理链接点击事件
        if (href != null) {
          _launchUrl(href);
        }
      },
      styleSheet: MarkdownStyleSheet(
        // 标题样式
        h1: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        h2: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
        h3: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        
        // 段落样式
        p: const TextStyle(fontSize: 16, height: 1.5),
        
        // 列表样式
        listBullet: const TextStyle(color: Colors.blue),
        
        // 代码样式
        code: const TextStyle(
          fontFamily: 'monospace',
          fontSize: 14,
          backgroundColor: Color(0xFFEEEEEE),
        ),
        
        // 代码块样式
        codeblockPadding: const EdgeInsets.all(16),
        codeblockDecoration: BoxDecoration(
          color: const Color(0xFFEEEEEE),
          borderRadius: BorderRadius.circular(4),
        ),
      ),
    );
  }

  // 打开链接
  void _launchUrl(String url) async {
    final uri = Uri.parse(url);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri);
    } else {
      throw 'Could not launch $url';
    }
  }
}
```

### 3. 更新文章详情页面

#### 更新 screens/article_detail_screen.dart
```dart
import 'package:flutter/material.dart';
import '../models/article.dart';
import '../components/markdown_viewer.dart';

class ArticleDetailPage extends StatelessWidget {
  final Article article;

  const ArticleDetailPage({Key? key, required this.article}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          article.title,
          style: const TextStyle(fontSize: 16),
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
      body: SingleChildScrollView(
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
      ),
    );
  }

  // 格式化日期
  String _formatDate(DateTime date) {
    return '${date.year}-${date.month.toString().padLeft(2, '0')}-${date.day.toString().padLeft(2, '0')}';
  }
}
```

### 4. 更新主页面以支持 Markdown 内容预览

#### 更新 lib/main.dart
```dart
import 'package:flutter/material.dart';
import 'components/article_card.dart';
import 'models/article.dart';
import 'services/api_service.dart';
import 'screens/article_detail_screen.dart';

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

### 5. 添加 url_launcher 依赖处理链接

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
  url_launcher: ^6.1.7  # 添加链接处理包

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

### 6. 更新项目结构
```
lib/
├── main.dart
├── components/
│   ├── article_card.dart
│   └── markdown_viewer.dart
├── models/
│   └── article.dart
├── services/
│   └── api_service.dart
├── screens/
│   └── article_detail_screen.dart
```

## 易错点及解决方案

### 1. Markdown 样式不生效
**问题：**
自定义样式未正确应用

**解决方案：**
确保 MarkdownStyleSheet 正确配置，优先级高于默认样式

### 2. 链接无法打开
**问题：**
Markdown 中的链接点击无反应

**解决方案：**
实现 onTapLink 回调，并使用 url_launcher 打开链接

### 3. 代码块显示异常
**问题：**
代码块字体或背景色不符合预期

**解决方案：**
检查 fontFamily 设置，确保使用等宽字体

### 4. 图片无法显示
**问题：**
Markdown 中的图片链接无法加载

**解决方案：**
flutter_markdown 默认不支持图片加载，需要自定义 ImageBuilder

## 今日任务检查清单
- [ ] 添加 flutter_markdown 和 url_launcher 依赖
- [ ] 创建 Markdown 渲染组件
- [ ] 更新文章详情页以支持 Markdown 渲染
- [ ] 实现链接点击处理
- [ ] 自定义 Markdown 样式

## 扩展阅读
- [flutter_markdown 包文档](https://pub.dev/packages/flutter_markdown)
- [Markdown 语法指南](https://guides.github.com/features/mastering-markdown/)
- [url_launcher 包文档](https://pub.dev/packages/url_launcher)