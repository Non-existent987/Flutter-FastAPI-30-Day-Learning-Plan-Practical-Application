# Day 20 详细学习计划：内容生产与核心功能完善

## 学习目标
- 完善网站核心内容
- 实现 GitHub 代码同步
- 优化内容管理系统
- 准备 MVP 版本发布

## 知识点详解

### 1. 内容管理系统
**功能需求：**
- 内容创建和编辑
- 版本控制
- 发布管理
- 分类标签

**实现方式：**
- 直接操作数据库
- 通过 API 管理
- 集成第三方 CMS

### 2. GitHub 集成
**集成方式：**
- GitHub API
- Webhooks
- Actions 自动化

**应用场景：**
- 代码同步
- 自动部署
- 版本管理

### 3. MVP 版本准备
**核心功能：**
- 文章浏览
- Markdown 渲染
- 响应式设计
- 基础交互

**质量要求：**
- 功能完整性
- 性能达标
- 用户体验良好

## 练习代码

### 1. 创建内容管理服务

#### 创建 services/content_manager.dart
```dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:my_tutorial_site/models/article.dart';

class ContentManager {
  static const String _baseUrl = 'http://localhost:8000';
  static const String _articlesEndpoint = '/articles/';
  
  // 获取所有文章
  static Future<List<Article>> getAllArticles() async {
    final response = await http.get(
      Uri.parse('$_baseUrl$_articlesEndpoint'),
    );
    
    if (response.statusCode == 200) {
      final List<dynamic> jsonData = json.decode(response.body);
      return jsonData.map((data) => Article.fromJson(data)).toList();
    } else {
      throw Exception('获取文章列表失败: ${response.statusCode}');
    }
  }
  
  // 创建新文章
  static Future<Article> createArticle(Article article) async {
    final response = await http.post(
      Uri.parse('$_baseUrl$_articlesEndpoint'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(article.toJson()),
    );
    
    if (response.statusCode == 201) {
      final jsonData = json.decode(response.body);
      return Article.fromJson(jsonData);
    } else {
      throw Exception('创建文章失败: ${response.statusCode}');
    }
  }
  
  // 更新文章
  static Future<Article> updateArticle(Article article) async {
    final response = await http.put(
      Uri.parse('$_baseUrl$_articlesEndpoint${article.id}'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(article.toJson()),
    );
    
    if (response.statusCode == 200) {
      final jsonData = json.decode(response.body);
      return Article.fromJson(jsonData);
    } else {
      throw Exception('更新文章失败: ${response.statusCode}');
    }
  }
  
  // 删除文章
  static Future<bool> deleteArticle(int articleId) async {
    final response = await http.delete(
      Uri.parse('$_baseUrl$_articlesEndpoint$articleId'),
    );
    
    if (response.statusCode == 200) {
      return true;
    } else {
      throw Exception('删除文章失败: ${response.statusCode}');
    }
  }
  
  // 根据 ID 获取文章
  static Future<Article> getArticleById(int id) async {
    final response = await http.get(
      Uri.parse('$_baseUrl$_articlesEndpoint$id'),
    );
    
    if (response.statusCode == 200) {
      final jsonData = json.decode(response.body);
      return Article.fromJson(jsonData);
    } else {
      throw Exception('获取文章失败: ${response.statusCode}');
    }
  }
}
```

### 2. 创建 GitHub 集成服务

#### 创建 services/github_service.dart
```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class GithubService {
  static const String _baseUrl = 'https://api.github.com';
  static const String _owner = 'your-github-username'; // 替换为你的 GitHub 用户名
  static const String _repo = 'flutter-fast'; // 替换为你的仓库名
  
  // 获取仓库信息
  static Future<Map<String, dynamic>> getRepositoryInfo() async {
    final response = await http.get(
      Uri.parse('$_baseUrl/repos/$_owner/$_repo'),
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('获取仓库信息失败: ${response.statusCode}');
    }
  }
  
  // 获取仓库内容
  static Future<List<dynamic>> getRepositoryContents([String path = '']) async {
    final response = await http.get(
      Uri.parse('$_baseUrl/repos/$_owner/$_repo/contents/$path'),
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('获取仓库内容失败: ${response.statusCode}');
    }
  }
  
  // 获取特定文件内容
  static Future<String> getFileContent(String filePath) async {
    final response = await http.get(
      Uri.parse('$_baseUrl/repos/$_owner/$_repo/contents/$filePath'),
    );
    
    if (response.statusCode == 200) {
      final jsonData = json.decode(response.body);
      // GitHub API 返回的是 base64 编码的内容
      final content = jsonData['content'];
      // 解码 base64
      return utf8.decode(base64Decode(content));
    } else {
      throw Exception('获取文件内容失败: ${response.statusCode}');
    }
  }
  
  // 获取提交历史
  static Future<List<dynamic>> getCommits([int limit = 10]) async {
    final response = await http.get(
      Uri.parse('$_baseUrl/repos/$_owner/$_repo/commits?per_page=$limit'),
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('获取提交历史失败: ${response.statusCode}');
    }
  }
}
```

### 3. 创建关于页面

#### 创建 screens/about_screen.dart
```dart
import 'package:flutter/material.dart';
import 'package:my_tutorial_site/components/fade_animation.dart';
import 'package:my_tutorial_site/services/github_service.dart';
import 'package:my_tutorial_site/components/loading_indicator.dart';
import 'package:my_tutorial_site/components/error_display.dart';

class AboutScreen extends StatefulWidget {
  const AboutScreen({Key? key}) : super(key: key);

  @override
  State<AboutScreen> createState() => _AboutScreenState();
}

class _AboutScreenState extends State<AboutScreen> {
  Future<Map<String, dynamic>>? _repoInfoFuture;
  Future<List<dynamic>>? _commitsFuture;

  @override
  void initState() {
    super.initState();
    _loadGithubData();
  }

  void _loadGithubData() {
    setState(() {
      _repoInfoFuture = GithubService.getRepositoryInfo();
      _commitsFuture = GithubService.getCommits(5);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('关于我们'),
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const FadeAnimation(
                delay: Duration(milliseconds: 100),
                child: Text(
                  'Flutter + FastAPI 30天速成',
                  style: TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(height: 24),
              const FadeAnimation(
                delay: Duration(milliseconds: 200),
                child: Text(
                  '项目介绍',
                  style: TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(height: 16),
              const FadeAnimation(
                delay: Duration(milliseconds: 300),
                child: Text(
                  '这是一个"边学边做"的全栈实践计划，旨在通过30天时间，在工作之余掌握Flutter（前端）与FastAPI（后端），'
                  '并开发出一个名为"Flutter+FastAPI 30天速成"的教学网站。该网站本身即是学习成果的展示，'
                  '也是教他人如何在一个月内完成相同目标的教学平台。',
                  style: TextStyle(fontSize: 16, height: 1.6),
                ),
              ),
              const SizedBox(height: 24),
              const FadeAnimation(
                delay: Duration(milliseconds: 400),
                child: Text(
                  '核心技术栈',
                  style: TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(height: 16),
              const FadeAnimation(
                delay: Duration(milliseconds: 500),
                child: ListTile(
                  leading: Icon(Icons.code, color: Colors.blue),
                  title: Text('前端: Flutter Web'),
                  subtitle: Text('编译为HTML/JS/WASM'),
                ),
              ),
              const FadeAnimation(
                delay: Duration(milliseconds: 600),
                child: ListTile(
                  leading: Icon(Icons.api, color: Colors.green),
                  title: Text('后端: FastAPI'),
                  subtitle: Text('Python高性能Web框架'),
                ),
              ),
              const FadeAnimation(
                delay: Duration(milliseconds: 700),
                child: ListTile(
                  leading: Icon(Icons.storage, color: Colors.orange),
                  title: Text('数据库: SQLite'),
                  subtitle: Text('轻量级文件型数据库'),
                ),
              ),
              const FadeAnimation(
                delay: Duration(milliseconds: 800),
                child: ListTile(
                  leading: Icon(Icons.cloud_upload, color: Colors.purple),
                  title: Text('部署: Docker + Nginx'),
                  subtitle: Text('容器化部署方案'),
                ),
              ),
              const SizedBox(height: 24),
              const FadeAnimation(
                delay: Duration(milliseconds: 900),
                child: Text(
                  'GitHub 仓库信息',
                  style: TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(height: 16),
              FutureBuilder<Map<String, dynamic>>(
                future: _repoInfoFuture,
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return const LoadingIndicator(message: '加载仓库信息...');
                  } else if (snapshot.hasError) {
                    return ErrorDisplay(
                      message: '加载仓库信息失败: ${snapshot.error}',
                      onRetry: _loadGithubData,
                    );
                  } else if (snapshot.hasData) {
                    final repoInfo = snapshot.data!;
                    return FadeAnimation(
                      delay: const Duration(milliseconds: 1000),
                      child: Card(
                        child: Padding(
                          padding: const EdgeInsets.all(16.0),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                repoInfo['full_name'] ?? '未知仓库',
                                style: const TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              const SizedBox(height: 8),
                              Text(repoInfo['description'] ?? '暂无描述'),
                              const SizedBox(height: 16),
                              Row(
                                children: [
                                  Icon(Icons.star, 
                                    color: Theme.of(context).brightness == Brightness.light 
                                        ? Colors.amber 
                                        : Colors.amber[300]),
                                  const SizedBox(width: 4),
                                  Text('${repoInfo['stargazers_count'] ?? 0} Stars'),
                                  const SizedBox(width: 16),
                                  const Icon(Icons.remove_red_eye, color: Colors.grey),
                                  const SizedBox(width: 4),
                                  Text('${repoInfo['watchers_count'] ?? 0} Watchers'),
                                  const SizedBox(width: 16),
                                  const Icon(Icons.merge_type, color: Colors.green),
                                  const SizedBox(width: 4),
                                  Text('${repoInfo['forks_count'] ?? 0} Forks'),
                                ],
                              ),
                              const SizedBox(height: 16),
                              Text(
                                '最后更新: ${(DateTime.tryParse(repoInfo['updated_at'] ?? '') ?? DateTime.now()).toString().split(' ')[0]}',
                                style: const TextStyle(color: Colors.grey),
                              ),
                            ],
                          ),
                        ),
                      ),
                    );
                  } else {
                    return const Center(child: Text('暂无仓库信息'));
                  }
                },
              ),
              const SizedBox(height: 24),
              const FadeAnimation(
                delay: Duration(milliseconds: 1100),
                child: Text(
                  '最近提交',
                  style: TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(height: 16),
              FutureBuilder<List<dynamic>>(
                future: _commitsFuture,
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return const LoadingIndicator(message: '加载提交历史...');
                  } else if (snapshot.hasError) {
                    return ErrorDisplay(
                      message: '加载提交历史失败: ${snapshot.error}',
                      onRetry: _loadGithubData,
                    );
                  } else if (snapshot.hasData) {
                    final commits = snapshot.data!;
                    return ListView.builder(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      itemCount: commits.length,
                      itemBuilder: (context, index) {
                        final commit = commits[index];
                        final commitInfo = commit['commit'];
                        return FadeAnimation(
                          delay: Duration(milliseconds: 1200 + (index * 100)),
                          child: Card(
                            child: ListTile(
                              title: Text(commitInfo['message']),
                              subtitle: Text(
                                '${commit['author']['login'] ?? 'Unknown'} '
                                '于 ${(DateTime.tryParse(commitInfo['author']['date'] ?? '') ?? DateTime.now()).toString().split(' ')[0]}',
                              ),
                              trailing: const Icon(Icons.commit),
                            ),
                          ),
                        );
                      },
                    );
                  } else {
                    return const Center(child: Text('暂无提交历史'));
                  }
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### 4. 更新路由配置添加关于页面

#### 更新 router/app_router.dart
```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:my_tutorial_site/screens/home_screen.dart';
import 'package:my_tutorial_site/screens/article_detail_screen.dart';
import 'package:my_tutorial_site/screens/about_screen.dart';
import 'package:my_tutorial_site/models/article.dart';

// 定义路由名称常量
abstract class AppRoutes {
  static const home = 'home';
  static const articleDetail = 'articleDetail';
  static const about = 'about';
}

final GoRouter router = GoRouter(
  routes: [
    GoRoute(
      name: AppRoutes.home,
      path: '/',
      builder: (context, state) => const HomeScreen(),
    ),
    GoRoute(
      name: AppRoutes.articleDetail,
      path: '/article/:id',
      builder: (context, state) {
        // 获取路径参数
        final articleId = int.parse(state.pathParameters['id']!);
        
        // 获取额外参数（如果有的话）
        final article = state.extra as Article?;
        
        return ArticleDetailPage(
          articleId: articleId,
          article: article,
        );
      },
    ),
    GoRoute(
      name: AppRoutes.about,
      path: '/about',
      builder: (context, state) => const AboutScreen(),
    ),
  ],
  
  errorBuilder: (context, state) => Scaffold(
    appBar: AppBar(title: const Text('页面未找到')),
    body: Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Text('抱歉，您访问的页面不存在'),
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: () => context.go('/'),
            child: const Text('返回首页'),
          ),
        ],
      ),
    ),
  ),
);
```

### 5. 更新主页添加关于页面入口

#### 更新 screens/home_screen.dart（部分更新）
```dart
// 在 Drawer 中添加关于页面入口
Drawer(
  child: ListView(
    padding: EdgeInsets.zero,
    children: [
      const DrawerHeader(
        decoration: BoxDecoration(
          color: Color(0xFF2196F3),
        ),
        child: Text(
          '课程目录',
          style: TextStyle(
            color: Colors.white,
            fontSize: 24,
          ),
        ),
      ),
      ListTile(
        leading: const Icon(Icons.home),
        title: const Text('首页'),
        onTap: () {
          HapticFeedbackService().lightImpact();
          Navigator.pop(context);
        },
      ),
      const Divider(),
      ListTile(
        leading: const Icon(Icons.book),
        title: const Text('第1周：后端基础'),
        onTap: () {
          HapticFeedbackService().lightImpact();
          Navigator.pop(context);
        },
      ),
      ListTile(
        leading: const Icon(Icons.book),
        title: const Text('第2周：前端基础'),
        onTap: () {
          HapticFeedbackService().lightImpact();
          Navigator.pop(context);
        },
      ),
      ListTile(
        leading: const Icon(Icons.book),
        title: const Text('第3周：全栈整合'),
        onTap: () {
          HapticFeedbackService().lightImpact();
          Navigator.pop(context);
        },
      ),
      ListTile(
        leading: const Icon(Icons.book),
        title: const Text('第4周：部署上线'),
        onTap: () {
          HapticFeedbackService().lightImpact();
          Navigator.pop(context);
        },
      ),
      const Divider(),
      ListTile(
        leading: const Icon(Icons.info),
        title: const Text('关于我们'),
        onTap: () {
          HapticFeedbackService().lightImpact();
          Navigator.pop(context);
          context.push('/about');
        },
      ),
    ],
  ),
),
```

### 6. 更新项目结构
```
lib/
├── main.dart
├── components/
│   ├── article_card.dart
│   ├── error_boundary.dart
│   ├── error_display.dart
│   ├── fade_animation.dart
│   ├── loading_indicator.dart
│   ├── markdown_viewer.dart
│   ├── network_aware_widget.dart
│   ├── retry_future_builder.dart
│   ├── search_bar.dart
│   └── skeleton_loader.dart
├── models/
│   └── article.dart
├── router/
│   └── app_router.dart
├── screens/
│   ├── about_screen.dart
│   ├── article_detail_screen.dart
│   ├── home_screen.dart
│   └── search_results_screen.dart
├── services/
│   ├── api_service.dart
│   ├── connectivity_service.dart
│   ├── content_manager.dart
│   ├── github_service.dart
│   └── haptic_feedback_service.dart
├── themes/
│   └── app_theme.dart
```

## 易错点及解决方案

### 1. GitHub API 速率限制
**问题：**
匿名请求速率受限

**解决方案：**
使用 GitHub Token 进行认证请求，或实现缓存机制

### 2. 内容同步时机
**问题：**
代码更新后内容未及时同步

**解决方案：**
使用 GitHub Webhooks 实现实时同步，或定时轮询

### 3. 错误处理不完善
**问题：**
网络请求失败时用户体验差

**解决方案：**
提供详细的错误信息和重试机制

### 4. 数据一致性
**问题：**
本地和远程数据不一致

**解决方案：**
实现数据同步机制，确保数据一致性

## 今日任务检查清单
- [ ] 创建内容管理服务
- [ ] 实现 GitHub 集成服务
- [ ] 创建关于页面展示项目信息
- [ ] 更新路由配置和导航
- [ ] 测试核心功能完整性

## 扩展阅读
- [GitHub API 文档](https://docs.github.com/en/rest)
- [内容管理系统设计](https://en.wikipedia.org/wiki/Content_management_system)
- [MVP 开发模式](https://en.wikipedia.org/wiki/Minimum_viable_product)