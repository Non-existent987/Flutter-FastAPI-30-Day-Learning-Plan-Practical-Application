import 'package:flutter/material.dart';
import 'components/article_card.dart';
import 'components/expandable_article_card.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Tutorial Site',
      theme: ThemeData(primarySwatch: Colors.blue), //
      home: const TutorialHomePage(),
    );
  }
}

class TutorialHomePage extends StatelessWidget {
  const TutorialHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    // 模拟文章数据 final的作用是避免重复创建数据，final的定义是创建一个常量，常量不能被修改
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
      appBar: AppBar(title: const Text('Flutter + FastAPI 教程网站')),
      body: Row(
        children: [
          // 左侧导航栏
          // Expande的定义是创建一个可扩展的布局，它可以根据子组件的宽度进行扩展。
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
                      // T ODO: 导航到数据模型教程
                    },
                  ),
                  ListTile(
                    leading: const Icon(Icons.storage),
                    title: const Text('数据库集成'),
                    onTap: () {
                      // T ODO: 导航到数据库集成教程
                    },
                  ),
                  ListTile(
                    leading: const Icon(Icons.api),
                    title: const Text('CRUD 操作'),
                    onTap: () {
                      // T ODO: 导航到 CRUD 操作教程
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
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 16),
                  Expanded(
                    child: ListView.builder(
                      itemCount: articles.length,
                      itemBuilder: (context, index) {
                        final article = articles[index];
                        return ArticleCard(
                          title: article['title']! as String,
                          summary: article['summary'] as String,
                          author: article['author'] as String?,
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
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
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
