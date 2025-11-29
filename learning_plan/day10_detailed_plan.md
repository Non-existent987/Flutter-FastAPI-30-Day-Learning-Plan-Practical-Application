# Day 10 详细学习计划：组件化开发实践

## 学习目标
- 理解 StatelessWidget 和 StatefulWidget
- 学习组件化开发思想
- 创建可复用的文章卡片组件
- 实现组件间通信

## 知识点详解

### 1. StatelessWidget vs StatefulWidget
**StatelessWidget：**
- 不可变的 Widget
- 一旦创建就不能改变
- 适用于静态内容

**StatefulWidget：**
- 可变的 Widget
- 有状态管理能力
- 适用于交互式内容

### 2. 组件化开发思想
**核心理念：**
- 单一职责原则：每个组件只负责一项功能
- 可复用性：组件可以在多处使用
- 可组合性：通过组合小组件构建复杂界面

**优势：**
- 提高开发效率
- 便于维护和调试
- 促进团队协作

### 3. 组件生命周期
**StatelessWidget 生命周期：**
1. 构造函数调用
2. build 方法执行

**StatefulWidget 生命周期：**
1. createState 方法
2. initState 方法（初始化状态）
3. build 方法（构建界面）
4. setState 方法（更新状态）
5. dispose 方法（销毁资源）

## 练习代码

### 1. 文章卡片组件 ArticleCard

#### 创建 components/article_card.dart
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

### 2. 可展开的文章卡片 ExpandableArticleCard

#### 创建 components/expandable_article_card.dart
```dart
import 'package:flutter/material.dart';

class ExpandableArticleCard extends StatefulWidget {
  final String title;
  final String content;
  final String? author;

  const ExpandableArticleCard({
    Key? key,
    required this.title,
    required this.content,
    this.author,
  }) : super(key: key);

  @override
  State<ExpandableArticleCard> createState() => _ExpandableArticleCardState();
}

class _ExpandableArticleCardState extends State<ExpandableArticleCard> {
  bool _isExpanded = false;

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      margin: const EdgeInsets.all(8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          ListTile(
            title: Text(
              widget.title,
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
            subtitle: widget.author != null ? Text('作者: ${widget.author}') : null,
            trailing: IconButton(
              icon: Icon(
                _isExpanded ? Icons.expand_less : Icons.expand_more,
              ),
              onPressed: () {
                setState(() {
                  _isExpanded = !_isExpanded;
                });
              },
            ),
          ),
          if (_isExpanded)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: Text(widget.content),
            ),
        ],
      ),
    );
  }
}
```

### 3. 使用自定义组件

#### 更新 lib/main.dart
```dart
import 'package:flutter/material.dart';
import 'components/article_card.dart';
import 'components/expandable_article_card.dart';

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

class TutorialHomePage extends StatelessWidget {
  const TutorialHomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // 模拟文章数据
    final articles = [
      {
        'title': 'Day 1: 环境搭建',
        'summary': '学习如何安装 Python、FastAPI 和配置开发环境',
        'author': '教程作者',
        'published': true,
      },
      {
        'title': 'Day 2: 数据模型',
        'summary': '学习 Pydantic 和数据验证',
        'author': '教程作者',
        'published': true,
      },
      {
        'title': 'Day 3: 数据库集成',
        'summary': '学习 SQLite 和 SQLModel 的使用',
        'author': '教程作者',
        'published': false,
      },
    ];

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
                    child: ListView.builder(
                      itemCount: articles.length,
                      itemBuilder: (context, index) {
                        final article = articles[index];
                        return ArticleCard(
                          title: article['title']!,
                          summary: article['summary']!,
                          author: article['author'],
                          isPublished: article['published'] as bool,
                          onTap: () {
                            // 点击文章卡片的处理
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(
                                content: Text('打开文章: ${article['title']}'),
                              ),
                            );
                          },
                        );
                      },
                    ),
                  ),
                  const SizedBox(height: 32),
                  const Text(
                    '可展开卡片示例',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 16),
                  const ExpandableArticleCard(
                    title: '什么是 Flutter?',
                    content:
                        'Flutter 是 Google 开源的 UI 工具包，用于从单一代码库为移动、Web 和桌面构建美观的原生编译应用程序。',
                    author: 'Google',
                  ),
                  const SizedBox(height: 16),
                  const ExpandableArticleCard(
                    title: '什么是 FastAPI?',
                    content:
                        'FastAPI 是一个现代、快速（高性能）的 Python Web 框架，用于构建 API，基于标准的 Python 类型提示。',
                    author: 'Sebastián Ramírez',
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

### 4. 创建组件目录结构
```
lib/
├── main.dart
├── components/
│   ├── article_card.dart
│   └── expandable_article_card.dart
```

## 易错点及解决方案

### 1. 组件状态管理混乱
**问题：**
应该使用 StatelessWidget 的地方使用了 StatefulWidget

**解决方案：**
根据组件是否需要状态变化来选择合适的 Widget 类型

### 2. 组件通信问题
**问题：**
父子组件间无法传递数据或回调

**解决方案：**
通过构造函数传递数据，通过回调函数传递事件

### 3. 内存泄漏
**问题：**
StatefulWidget 未正确释放资源

**解决方案：**
在 dispose 方法中释放资源，取消订阅等

### 4. 组件复用性差
**问题：**
组件过于具体，难以在其他地方使用

**解决方案：**
通过参数化提高组件灵活性，遵循单一职责原则

## 今日任务检查清单
- [ ] 理解 StatelessWidget 和 StatefulWidget 的区别
- [ ] 创建可复用的文章卡片组件
- [ ] 实现可展开的文章卡片组件
- [ ] 在主界面中使用自定义组件
- [ ] 理解组件化开发的优势

## 扩展阅读
- [Flutter 组件指南](https://flutter.dev/docs/development/ui/widgets)
- [StatefulWidget 生命周期](https://api.flutter.dev/flutter/widgets/StatefulWidget-class.html)
- [组件设计最佳实践](https://flutter.dev/docs/development/ui/layout)