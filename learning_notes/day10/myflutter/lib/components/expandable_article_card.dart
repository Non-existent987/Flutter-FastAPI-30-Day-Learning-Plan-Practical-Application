import 'package:flutter/material.dart';

// ExpandableArticleCard是一个有状态组件（StatefulWidget）
// 有状态组件意味着它内部可以保存和管理状态，并在状态改变时重新构建UI
// 这个组件用于展示可展开/折叠的文章卡片
class ExpandableArticleCard extends StatefulWidget {
  // 文章标题
  final String title;
  // 文章内容
  final String content;
  // 文章作者（可为空）
  final String? author;

  // 构造函数：定义组件需要的参数
  const ExpandableArticleCard({
    Key? key,
    required this.title,
    required this.content,
    this.author,
  }) : super(key: key);

  // 重写createState方法，返回与该组件关联的状态对象
  @override
  State<ExpandableArticleCard> createState() => _ExpandableArticleCardState();
}

// _ExpandableArticleCardState是与ExpandableArticleCard关联的状态类
// 下划线前缀表示这是私有类，只能在当前文件内访问
class _ExpandableArticleCardState extends State<ExpandableArticleCard> {
  // 定义一个布尔变量_isExpanded用于跟踪卡片是否展开
  bool _isExpanded = false;

  // build方法定义了组件的UI结构
  @override
  Widget build(BuildContext context) {
    // Card组件提供了卡片式的视觉效果
    return Card(
      // elevation设置卡片的阴影高度，值越大阴影越明显
      elevation: 4,
      // margin设置卡片外边距
      margin: const EdgeInsets.all(8),
      // Column组件用于垂直排列子组件
      child: Column(
        // crossAxisAlignment定义子组件在交叉轴上的对齐方式
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // ListTile是列表项的标准组件，常用于显示主要信息和次要信息
          ListTile(
            // title设置主要文本内容，这里是文章标题
            title: Text(
              widget.title,
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
            // subtitle设置次要文本内容，这里是作者信息
            // 使用条件表达式：如果作者信息存在则显示，否则为null不显示
            subtitle: widget.author != null
                ? Text('作者: ${widget.author}')
                : null,
            // trailing设置尾部控件，这里放置一个展开/折叠按钮
            trailing: IconButton(
              // icon根据_isExpanded状态决定显示展开还是折叠图标
              icon: Icon(_isExpanded ? Icons.expand_less : Icons.expand_more),
              // onPressed定义按钮点击事件处理函数
              onPressed: () {
                // setState方法用于更新组件状态并触发UI重建
                // 当_isExpanded值发生变化时，整个组件会重新构建
                setState(() {
                  // 切换展开状态：true变false，false变true
                  _isExpanded = !_isExpanded;
                });
              },
            ),
          ),
          // 条件渲染：只有当卡片处于展开状态时才显示文章内容
          if (_isExpanded)
            // Padding组件用于设置内容的内边距
            Padding(
              // 设置水平方向内边距16像素，垂直方向内边距8像素
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              // Text组件用于显示文章内容
              child: Text(widget.content),
            ),
        ],
      ),
    );
  }
}