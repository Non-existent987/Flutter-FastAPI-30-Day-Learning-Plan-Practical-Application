# Day 16 详细学习计划：UI 美化与主题定制

## 学习目标
- 学习 Flutter 主题系统
- 美化应用界面
- 自定义颜色和字体
- 添加视觉效果和动画

## 知识点详解

### 1. Flutter 主题系统
**MaterialApp 主题：**
- ThemeData：定义应用整体主题
- ColorScheme：定义颜色方案
- TextTheme：定义文本样式

**组件级主题：**
- 使用 Theme Widget 覆盖局部主题
- 自定义组件样式

### 2. 颜色系统
**颜色类型：**
- Primary Color：主色调
- Secondary Color：辅助色调
- Accent Color：强调色
- Surface Color：表面颜色

**颜色使用原则：**
- 保持一致性
- 考虑可访问性
- 遵循 Material Design 指南

### 3. 动画和过渡效果
**隐式动画：**
- AnimatedContainer
- AnimatedOpacity
- AnimatedPadding

**显式动画：**
- AnimationController
- Tween
- AnimatedBuilder

## 练习代码

### 1. 创建自定义主题

#### 创建 themes/app_theme.dart
```dart
import 'package:flutter/material.dart';

class AppTheme {
  static final lightTheme = ThemeData(
    useMaterial3: true,
    brightness: Brightness.light,
    primaryColor: const Color(0xFF2196F3),
    scaffoldBackgroundColor: const Color(0xFFF5F5F5),
    appBarTheme: const AppBarTheme(
      color: Color(0xFF2196F3),
      elevation: 0,
      titleTextStyle: TextStyle(
        color: Colors.white,
        fontSize: 20,
        fontWeight: FontWeight.bold,
      ),
      iconTheme: IconThemeData(color: Colors.white),
    ),
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF2196F3),
      brightness: Brightness.light,
    ),
    textTheme: const TextTheme(
      headlineLarge: TextStyle(
        fontSize: 32,
        fontWeight: FontWeight.bold,
        color: Colors.black87,
      ),
      headlineMedium: TextStyle(
        fontSize: 24,
        fontWeight: FontWeight.bold,
        color: Colors.black87,
      ),
      headlineSmall: TextStyle(
        fontSize: 20,
        fontWeight: FontWeight.bold,
        color: Colors.black87,
      ),
      bodyLarge: TextStyle(
        fontSize: 16,
        color: Colors.black87,
      ),
      bodyMedium: TextStyle(
        fontSize: 14,
        color: Colors.black54,
      ),
    ),
    cardTheme: CardTheme(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        foregroundColor: Colors.white,
        backgroundColor: const Color(0xFF2196F3),
        textStyle: const TextStyle(
          fontSize: 16,
          fontWeight: FontWeight.bold,
        ),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        padding: const EdgeInsets.symmetric(
          horizontal: 24,
          vertical: 12,
        ),
      ),
    ),
  );

  static final darkTheme = ThemeData(
    useMaterial3: true,
    brightness: Brightness.dark,
    primaryColor: const Color(0xFF2196F3),
    scaffoldBackgroundColor: const Color(0xFF121212),
    appBarTheme: const AppBarTheme(
      color: Color(0xFF1E88E5),
      elevation: 0,
      titleTextStyle: TextStyle(
        color: Colors.white,
        fontSize: 20,
        fontWeight: FontWeight.bold,
      ),
      iconTheme: IconThemeData(color: Colors.white),
    ),
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF2196F3),
      brightness: Brightness.dark,
    ),
    textTheme: const TextTheme(
      headlineLarge: TextStyle(
        fontSize: 32,
        fontWeight: FontWeight.bold,
        color: Colors.white70,
      ),
      headlineMedium: TextStyle(
        fontSize: 24,
        fontWeight: FontWeight.bold,
        color: Colors.white70,
      ),
      headlineSmall: TextStyle(
        fontSize: 20,
        fontWeight: FontWeight.bold,
        color: Colors.white70,
      ),
      bodyLarge: TextStyle(
        fontSize: 16,
        color: Colors.white70,
      ),
      bodyMedium: TextStyle(
        fontSize: 14,
        color: Colors.white54,
      ),
    ),
    cardTheme: CardTheme(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        foregroundColor: Colors.white,
        backgroundColor: const Color(0xFF1E88E5),
        textStyle: const TextStyle(
          fontSize: 16,
          fontWeight: FontWeight.bold,
        ),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        padding: const EdgeInsets.symmetric(
          horizontal: 24,
          vertical: 12,
        ),
      ),
    ),
  );
}
```

### 2. 更新主应用文件以使用自定义主题

#### 更新 lib/main.dart
```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'components/error_boundary.dart';
import 'router/app_router.dart';
import 'themes/app_theme.dart';

void main() {
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
                    Text('错误信息: $error'),
                    const SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: () {
                        // 重启应用
                        context.go('/');
                      },
                      child: const Text('返回首页'),
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

### 3. 美化文章卡片组件

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
    final theme = Theme.of(context);
    
    return Card(
      elevation: 2,
      margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
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
                      style: theme.textTheme.headlineSmall?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  if (!isPublished)
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 8,
                        vertical: 4,
                      ),
                      decoration: BoxDecoration(
                        color: Colors.orange.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: const Text(
                        '草稿',
                        style: TextStyle(
                          color: Colors.orange,
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                ],
              ),
              const SizedBox(height: 8),
              Text(
                summary,
                style: theme.textTheme.bodyMedium,
                maxLines: 3,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 12),
              if (author != null)
                Row(
                  children: [
                    const Icon(
                      Icons.person,
                      size: 16,
                      color: Colors.blue,
                    ),
                    const SizedBox(width: 4),
                    Text(
                      author!,
                      style: const TextStyle(
                        fontSize: 14,
                        color: Colors.blue,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ],
                ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### 4. 美化加载指示器组件

#### 更新 components/loading_indicator.dart
```dart
import 'package:flutter/material.dart';

class LoadingIndicator extends StatelessWidget {
  final String message;

  const LoadingIndicator({Key? key, this.message = '加载中...'}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          SizedBox(
            width: 48,
            height: 48,
            child: CircularProgressIndicator(
              strokeWidth: 3,
              valueColor: AlwaysStoppedAnimation<Color>(
                theme.colorScheme.primary,
              ),
            ),
          ),
          const SizedBox(height: 16),
          Text(
            message,
            style: theme.textTheme.bodyLarge,
          ),
        ],
      ),
    );
  }
}
```

### 5. 美化错误显示组件

#### 更新 components/error_display.dart
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
    final theme = Theme.of(context);
    
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: theme.colorScheme.error.withOpacity(0.1),
                shape: BoxShape.circle,
              ),
              child: Icon(
                Icons.error_outline,
                size: 48,
                color: theme.colorScheme.error,
              ),
            ),
            const SizedBox(height: 24),
            Text(
              message,
              textAlign: TextAlign.center,
              style: theme.textTheme.bodyLarge?.copyWith(
                color: theme.colorScheme.error,
              ),
            ),
            const SizedBox(height: 24),
            if (onRetry != null)
              ElevatedButton.icon(
                onPressed: onRetry,
                icon: const Icon(Icons.refresh),
                label: const Text('重试'),
              ),
          ],
        ),
      ),
    );
  }
}
```

### 6. 美化 Markdown 查看器组件

#### 更新 components/markdown_viewer.dart
```dart
import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:url_launcher/url_launcher.dart';

class MarkdownViewer extends StatelessWidget {
  final String markdownData;

  const MarkdownViewer({Key? key, required this.markdownData}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
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
        h1: theme.textTheme.headlineMedium?.copyWith(
          fontWeight: FontWeight.bold,
          color: theme.colorScheme.primary,
        ),
        h2: theme.textTheme.headlineSmall?.copyWith(
          fontWeight: FontWeight.bold,
          color: theme.colorScheme.primary,
        ),
        h3: theme.textTheme.titleLarge?.copyWith(
          fontWeight: FontWeight.bold,
          color: theme.colorScheme.primary,
        ),
        
        // 段落样式
        p: theme.textTheme.bodyLarge,
        
        // 列表样式
        listBullet: theme.textTheme.bodyLarge?.copyWith(
          color: theme.colorScheme.primary,
        ),
        
        // 代码样式
        code: TextStyle(
          fontFamily: 'monospace',
          fontSize: 14,
          color: theme.brightness == Brightness.dark 
              ? Colors.orange[300] 
              : Colors.orange[700],
          backgroundColor: theme.brightness == Brightness.dark
              ? Colors.grey[800]
              : Colors.grey[200],
        ),
        
        // 代码块样式
        codeblockPadding: const EdgeInsets.all(16),
        codeblockDecoration: BoxDecoration(
          color: theme.brightness == Brightness.dark
              ? Colors.grey[800]
              : Colors.grey[200],
          borderRadius: BorderRadius.circular(8),
        ),
        
        // 引用块样式
        blockquote: theme.textTheme.bodyLarge?.copyWith(
          color: theme.colorScheme.secondary,
          fontStyle: FontStyle.italic,
        ),
        blockquoteDecoration: BoxDecoration(
          color: theme.colorScheme.secondary.withOpacity(0.1),
          border: Border(
            left: BorderSide(
              color: theme.colorScheme.secondary,
              width: 4,
            ),
          ),
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

### 7. 更新项目结构
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
├── router/
│   └── app_router.dart
├── services/
│   └── api_service.dart
├── screens/
│   ├── article_detail_screen.dart
│   └── home_screen.dart
├── themes/
│   └── app_theme.dart
```

## 易错点及解决方案

### 1. 主题颜色不一致
**问题：**
深色和浅色主题颜色不协调

**解决方案：**
使用 ColorScheme.fromSeed 生成协调的颜色方案，或手动定义深色主题颜色

### 2. 文本可读性差
**问题：**
文本颜色与背景对比度不足

**解决方案：**
使用 Material Design 的颜色对比度指南，确保文本可读性

### 3. 组件样式冲突
**问题：**
局部样式与全局主题冲突

**解决方案：**
使用 Theme.of(context) 获取当前主题，或使用 Theme Widget 包装组件

### 4. 动画性能问题
**问题：**
过多动画导致性能下降

**解决方案：**
合理使用动画，避免在列表项中使用复杂动画，使用 RepaintBoundary 优化绘制

## 今日任务检查清单
- [ ] 创建自定义主题
- [ ] 美化文章卡片组件
- [ ] 优化加载和错误显示组件
- [ ] 改进 Markdown 渲染样式
- [ ] 实现深色主题支持

## 扩展阅读
- [Flutter 主题系统](https://flutter.dev/docs/cookbook/design/themes)
- [Material Design 颜色系统](https://material.io/design/color/the-color-system.html)
- [Flutter 动画教程](https://flutter.dev/docs/development/ui/animations)