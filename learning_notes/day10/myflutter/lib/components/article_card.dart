import 'package:flutter/material.dart';

// ArticleCard是一个无状态组件（StatelessWidget），用于展示文章卡片
// 它接收文章的各种属性并在界面上展示出来
class ArticleCard extends StatelessWidget {
  // 文章标题
  final String title;
  // 文章摘要
  final String summary;
  // 文章作者（可为空）
  final String? author;
  // 是否已发布
  final bool isPublished;
  // 点击回调函数
  final VoidCallback onTap;

  // 构造函数：定义组件需要的参数
  // required关键字表示这些参数是必须传入的
  const ArticleCard({
    Key? key,
    required this.title,
    required this.summary,
    this.author,
    this.isPublished = false,
    required this.onTap,
  }) : super(key: key);

  // build方法定义了组件的UI结构
  @override
  Widget build(BuildContext context) {
    // Card组件提供了卡片式的视觉效果
    return Card(
      // elevation设置卡片的阴影高度，值越大阴影越明显
      elevation: 4,
      // margin设置卡片外边距
      margin: const EdgeInsets.all(8),
      // InkWell组件用于处理触摸反馈（水波纹效果）
      child: InkWell(
        // onTap定义点击事件处理函数
        onTap: onTap,
        // Padding组件用于设置内边距
        child: Padding(
          // 设置四周内边距为16像素
          padding: const EdgeInsets.all(16),
          // Column组件用于垂直排列子组件
          child: Column(
            // crossAxisAlignment定义子组件在交叉轴上的对齐方式
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Row组件用于水平排列子组件
              Row(
                children: [
                  // Expanded组件用于填充剩余空间
                  Expanded(
                    child: Text(
                      // 显示文章标题
                      title,
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  // 条件渲染：如果文章未发布，则显示"草稿"标签
                  if (!isPublished)
                    const Chip(
                      // Chip是标签组件，通常用于显示简洁的信息
                      label: Text('草稿'),
                      // 设置标签背景色为橙色
                      backgroundColor: Colors.orange,
                    ),
                ],
              ),
              const SizedBox(height: 8),
              Text(
                summary,
                style: const TextStyle(fontSize: 14, color: Colors.grey),
                maxLines: 3,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 8),
              if (author != null)
                Text(
                  '作者: $author',
                  style: const TextStyle(fontSize: 12, color: Colors.blue),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
