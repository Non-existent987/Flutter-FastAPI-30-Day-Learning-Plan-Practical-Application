# Day 8 详细学习计划：Flutter 环境搭建与 Hello World

## 学习目标
- 安装 Flutter SDK
- 配置开发环境
- 创建第一个 Flutter 应用
- 运行计数器示例

## 知识点详解

### 1. Flutter 简介
**概念：**
- Google 开源的 UI 工具包
- 用于构建跨平台应用（iOS、Android、Web、桌面）
- 使用 Dart 语言开发

**优势：**
- 高性能（原生编译）
- 丰富的组件库
- 热重载功能
- 单一代码库多平台部署

### 2. Dart 语言基础
**特点：**
- 面向对象编程语言
- 类型安全（支持类型推断）
- 支持异步编程（async/await）
- 与 Flutter 深度集成

### 3. 开发环境配置
**必备工具：**
- Flutter SDK
- Android Studio 或 VS Code
- Android SDK（如果需要构建 Android 应用）
- Xcode（如果需要构建 iOS 应用，仅限 macOS）

## 练习代码

### 1. 安装 Flutter SDK

#### Windows 安装步骤：
1. 下载 Flutter SDK：https://flutter.dev/docs/get-started/install/windows
2. 解压到 C:\src\flutter
3. 添加环境变量：
   - 将 `C:\src\flutter\bin` 添加到 PATH

#### 验证安装：
```bash
flutter --version
```

### 2. 配置开发环境

#### VS Code 插件安装：
1. Flutter 插件
2. Dart 插件

#### 检查环境配置：
```bash
flutter doctor
```

### 3. 创建第一个 Flutter 应用

#### 创建项目：
```bash
flutter create my_tutorial_site
cd my_tutorial_site
```

#### 项目结构：
```
my_tutorial_site/
├── lib/
│   └── main.dart          # 应用入口文件
├── pubspec.yaml           # 项目配置文件
├── test/                  # 测试文件
└── web/                   # 平台特定代码
```

#### lib/main.dart（默认计数器应用）：
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
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'You have pushed the button this many times:',
            ),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.headline4,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

### 4. 运行应用

#### 运行在 Chrome 浏览器：
```bash
flutter run -d chrome
```

#### 运行在移动设备模拟器：
```bash
flutter run
```

## 易错点及解决方案

### 1. 环境变量配置问题
**问题：**
命令行无法识别 flutter 命令

**解决方案：**
确保 Flutter bin 目录已添加到系统 PATH 环境变量中

### 2. Android Studio 配置
**问题：**
flutter doctor 显示 Android toolchain 有问题

**解决方案：**
安装 Android Studio 并通过其安装 Android SDK

### 3. Web 支持未启用
**问题：**
无法运行在浏览器中

**解决方案：**
启用 Web 支持：
```bash
flutter config --enable-web
```

### 4. 端口被占用
**问题：**
Chrome 启动失败，端口被占用

**解决方案：**
指定其他端口：
```bash
flutter run -d chrome --web-port 3001
```

## 今日任务检查清单
- [ ] 安装 Flutter SDK
- [ ] 配置开发环境
- [ ] 创建第一个 Flutter 应用
- [ ] 成功运行计数器示例
- [ ] 理解基本的 Widget 结构

## 扩展阅读
- [Flutter 官方文档](https://flutter.dev/docs)
- [Dart 语言教程](https://dart.dev/guides)
- [Material Design 组件](https://material.io/components)