import 'package:flutter/material.dart';
import 'package:myflutter/components/article_card.dart';
// import 'components/article_card.dart';
import 'components/expandable_article_card.dart';

// 程序入口点：每个Flutter应用都需要一个main函数作为程序的起点
void main() {
  // runApp是Flutter框架提供的函数，用于启动应用程序
  // MyApp是我们自定义的应用根组件
  runApp(const MyApp());
}

// MyApp是一个无状态组件（StatelessWidget），表示应用的根组件
// 无状态组件意味着它的内容不会随时间变化
class MyApp extends StatelessWidget {
  // 构造函数，使用super.key将key传递给父类
  const MyApp({super.key});

  // build方法用于描述如何构建这个组件的UI
  @override
  Widget build(BuildContext context) {
    // MaterialApp是Flutter提供的Material Design风格的应用组件
    return MaterialApp(
      // 应用标题
      title: "Tutorial Site",
      // 应用主题，设置主色调为蓝色
      theme: ThemeData(primarySwatch: Colors.blue),
      // 应用首页，指向我们自定义的TutorialHomePage组件
      home: const TutorialHomePage(),
    );
  }
}

// TutorialHomePage是我们自定义的首页组件，也是一个无状态组件
class TutorialHomePage extends StatelessWidget {
  const TutorialHomePage({super.key});

  get title => null;

  // build方法定义了页面的具体UI结构
  @override
  Widget build(BuildContext context) {
    // 定义文章数据数组，模拟从服务器获取的文章列表
    // 每个文章包含标题、摘要、作者和发布状态等信息
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

    // Scaffold是Material Design的基本布局结构组件
    // 提供了应用栏、主体内容等标准界面元素
    return Scaffold(
      // 应用栏（顶部导航栏）
      appBar: AppBar(title: const Text("appbar")),
      // 页面主体内容，使用Row进行水平布局
      body: Row(
        children: [
          // 左侧边栏：占总宽度的3份
          Expanded(
            flex: 1,
            child: Container(
              // 设置背景色为琥珀色以便区分区域
              color: Colors.grey[300],
              // 使用ListView显示一个可滚动的列表
              child: ListView(
                children: [
                  // ListTile是列表项的标准组件
                  ListTile(
                    // leading属性设置列表项前面的图标
                    leading: const Icon(Icons.book),
                    // title属性设置列表项的标题文本
                    title: const Text("环境1搭建"),
                    // onTap属性定义点击事件的回调函数
                    onTap: () {
                      // 跳转
                      print('点击了环境搭建');
                    },
                  ),
                  ListTile(
                    leading: const Icon(Icons.book),
                    title: const Text("环境搭建2"),
                    onTap: () {
                      // 跳转
                      print('点击了环境搭建2');
                    },
                  ),
                  ListTile(
                    leading: const Icon(Icons.book),
                    title: const Text("环境搭建3"),
                    onTap: () {
                      // 跳转
                      print('点击了环境搭建2');
                    },
                  ),
                ],
              ),
            ),
          ),
          // 右侧主要内容区：同样占总宽度的3份
          Expanded(
            flex: 3,
            child: Container(
              // 添加内边距使内容不贴边
              padding: const EdgeInsets.all(16.0),
              child: Column(
                // crossAxisAlignment定义子组件在交叉轴上的对齐方式
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // 显示"最新教程"标题文本
                  const Text(
                    "最新教程",
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  // SizedBox用于创建固定大小的空间
                  const SizedBox(height: 16),

                  // 使用Expanded包装ListView.builder使其占据剩余空间
                  Expanded(
                    // ListView.builder是一种高效的列表构建方式
                    // 它只构建可见区域内的列表项，节省内存
                    child: ListView.builder(
                      // itemCount指定列表项的数量
                      itemCount: articles.length,
                      // itemBuilder是构建每个列表项的回调函数
                      itemBuilder: (context, index) {
                        // 获取当前索引对应的文章数据
                        final article = articles[index];
                        // 使用自定义的ArticleCard组件显示文章信息
                        return ArticleCard(
                          title: article['title']! as String,
                          summary: article['summary'] as String,
                          author: article['author'] as String?,
                          isPublished: article['published'] as bool,
                          // 定义点击事件处理函数
                          onTap: () {
                            // 使用SnackBar显示提示信息
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
                  // 显示"可展开卡片示例"标题
                  const Text(
                    "可展开卡片示例",
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 16),
                  // 使用自定义的可展开卡片组件展示内容
                  const ExpandableArticleCard(
                    title: "什么是 Flutter?",
                    content:
                        "Flutter 是 Google 开源的 UI 工具包，用于从单一代码库为移动、Web 和桌面构建美观的原生编译应用程序。",
                    author: "Google",
                  ),
                  const SizedBox(height: 16),
                  const ExpandableArticleCard(
                    title: "什么是 FastAPI?",
                    content:
                        "FastAPI 是一个现代、快速（高性能）的 Python Web 框架，用于构建 API，基于标准的 Python 类型提示。",
                    author: "Sebastián Ramírez",
                  ),
                  const SizedBox(height: 16),
                  const ExpandableArticleCard(
                    title: "什么是 Django?",
                    content: "Django 是一个用于快速开发 Web 应用程序的 Python Web 框架。",
                    author: "Django",
                  ),
                  const SizedBox(height: 16),
                  const ExpandableArticleCard(
                    title: "什么是 Flask?",
                    content: "Flask 是一个用于构建 Web 应用的 Python 框架。",
                    author: "Flask",
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
