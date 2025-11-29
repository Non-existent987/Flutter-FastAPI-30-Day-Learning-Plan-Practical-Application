# Day 9 详细学习计划：Dart 基础与 Flutter 布局

## 学习目标
- 学习 Dart 语言基础知识
- 理解 Flutter 布局系统
- 修改计数器应用界面
- 创建左右布局结构

## 知识点详解

### 1. Dart 语言基础
**核心概念：**
- 变量声明（var, final, const）
- 数据类型（int, double, String, bool, List, Map）
- 函数定义和调用
- 类和对象

### 2. Flutter 布局系统
**核心 Widgets：**
- Container：多功能容器
- Row：水平排列子元素
- Column：垂直排列子元素
- ListView：可滚动列表
- Expanded 和 Flexible：弹性布局

### 3. Widget 树概念
**重要性：**
- Flutter UI 由 Widget 构成
- Widget 是不可变的
- 通过组合构建复杂界面
- 父 Widget 控制子 Widget 的布局和行为

## 练习代码

### 1. Dart 基础语法

#### 变量和类型
```dart
// 变量声明
var name = '张三';
String title = 'Flutter 教程';
int count = 10;
double price = 99.99;
bool isPublished = true;

// Final 和 Const
final DateTime now = DateTime.now();  // 运行时常量
const double pi = 3.14159;            // 编译时常量

// 集合类型
List<String> topics = ['环境搭建', '数据模型', '数据库'];
Map<String, dynamic> article = {
  'title': 'Dart 基础',
  'author': '教程作者',
  'views': 1000,
};
```

#### 函数定义
```dart
// 基本函数
int add(int a, int b) {
  return a + b;
}

// 箭头函数（简洁语法）
int multiply(int a, int b) => a * b;

// 可选参数
String greet(String name, {String? title}) {
  if (title != null) {
    return 'Hello, $title $name!';
  }
  return 'Hello, $name!';
}

// 默认参数值
void printInfo(String name, {int age = 18}) {
  print('$name is $age years old');
}
```

#### 类和对象
```dart
class Article {
  String title;
  String content;
  String? author;
  bool published;
  
  // 构造函数
  Article(this.title, this.content, {this.author, this.published = false});
  
  // 命名构造函数
  Article.fromJson(Map<String, dynamic> json)
      : title = json['title'],
        content = json['content'],
        author = json['author'],
        published = json['published'] ?? false;
  
  // 方法
  void publish() {
    published = true;
    print('$title 已发布');
  }
  
  // Getter 和 Setter
  String get summary => content.substring(0, 50) + '...';
  
  // toString 方法
  @override
  String toString() {
    return 'Article(title: $title, author: $author, published: $published)';
  }
}
```

### 2. Flutter 布局实践

#### 修改后的 main.dart（左右布局）
```dart
import 'package:flutter/material.dart';

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
              child: SingleChildScrollView(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      '欢迎来到 Flutter + FastAPI 教程网站',
                      style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 16),
                    const Text(
                      '在这个网站中，您将学习如何使用 Flutter 和 FastAPI '
                      '构建一个完整的教程网站。本教程分为四个阶段：',
                      style: TextStyle(fontSize: 16),
                    ),
                    const SizedBox(height: 16),
                    const Text(
                      '1. 后端基础与数据核心 (FastAPI)',
                      style: TextStyle(fontSize: 16),
                    ),
                    const Text(
                      '2. 前端基础与页面构建 (Flutter)',
                      style: TextStyle(fontSize: 16),
                    ),
                    const Text(
                      '3. 全栈联调与内容填充',
                      style: TextStyle(fontSize: 16),
                    ),
                    const Text(
                      '4. 部署与上线',
                      style: TextStyle(fontSize: 16),
                    ),
                    const SizedBox(height: 32),
                    ElevatedButton(
                      onPressed: () {
                        // TODO: 开始学习按钮功能
                      },
                      child: const Text('开始学习'),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
```

### 3. 常用布局 Widgets

#### Container 示例
```dart
Container(
  width: 100,
  height: 100,
  margin: const EdgeInsets.all(10),
  padding: const EdgeInsets.all(8),
  decoration: BoxDecoration(
    color: Colors.blue,
    borderRadius: BorderRadius.circular(8),
  ),
  child: const Text('容器示例'),
)
```

#### Row 和 Column 示例
```dart
// 水平排列
Row(
  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
  children: [
    Icon(Icons.home),
    Icon(Icons.search),
    Icon(Icons.person),
  ],
)

// 垂直排列
Column(
  mainAxisAlignment: MainAxisAlignment.center,
  children: [
    Text('第一行'),
    Text('第二行'),
    Text('第三行'),
  ],
)
```

## 易错点及解决方案

### 1. 布局溢出问题
**问题：**
页面出现黄黑条纹警告

**解决方案：**
使用 SingleChildScrollView 包裹内容或调整布局约束

### 2. Expanded 使用错误
**问题：**
Expanded 不能在无约束的父 Widget 中使用

**解决方案：**
确保 Expanded 的父 Widget 是 Row、Column 或 Flex

### 3. 点击事件未响应
**问题：**
InkWell 或 GestureDetector 点击无反应

**解决方案：**
确保父 Widget 允许点击事件传递，或添加必要的约束

### 4. 字符串插值问题
**问题：**
表达式插值显示不正确

**解决方案：**
使用 ${expression} 语法，简单变量可省略大括号

## 今日任务检查清单
- [ ] 掌握 Dart 基础语法
- [ ] 理解 Flutter 布局系统
- [ ] 创建左右分割的页面布局
- [ ] 实现简单的导航菜单
- [ ] 理解 Widget 树结构

## 扩展阅读
- [Dart 语言指南](https://dart.dev/guides)
- [Flutter 布局教程](https://flutter.dev/docs/development/ui/layout)
- [Widget 目录](https://flutter.dev/docs/reference/widgets)