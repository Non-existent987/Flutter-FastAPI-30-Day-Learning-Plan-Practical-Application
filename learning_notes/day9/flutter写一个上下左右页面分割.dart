import 'package:flutter/material.dart';

// 程序入口点，main函数
void main() {
  // runApp是Flutter框架提供的顶层函数，用于启动应用程序
  runApp(
    // MaterialApp是Material Design风格的应用程序根组件
    MaterialApp(
      // 设置应用的标题
      title: "这是标题",
      // 设置应用的主题，这里设置了scaffold的背景色为红色
      theme: ThemeData(scaffoldBackgroundColor: Colors.red),
      // home属性指定应用默认显示的页面，这里是一个Scaffold组件
      home: Scaffold(
        // appBar属性定义应用栏（顶部导航栏）
        appBar: AppBar(
          // title属性设置应用栏的标题内容，使用Center居中显示文本
          title: Center(child: Text("这是标题")),
          // 添加颜色背景，设置应用栏背景色为黄色
          backgroundColor: Colors.yellow,
        ),
        // body属性定义页面的主要内容区域
        body: Row(
          // Row组件用于水平排列子组件
          children: [
            // 下面体现左侧导航栏右边的内容使用Expanded
            // Expanded组件用于在Row、Column或Flex中扩展子组件以填充可用空间
            Expanded(
              // flex属性定义了此组件相对于其他Expanded组件的弹性系数，这里占1份空间
              flex: 1,
              // Container是一个方便的容器组件，可以设置大小、颜色、边距等属性
              child: Container(
                // 设置容器背景色为绿色
                color: Colors.green,
                // ListView是一个可滚动的列表组件
                child: ListView(
                  // 子组件列表
                  children: [
                    // ListTile是Material Design中的列表项组件
                    ListTile(
                      // leading属性设置列表项前面的图标
                      leading: const Icon(Icons.book),
                      // title属性设置列表项的标题文本
                      title: const Text('环境搭建'),
                      // onTap属性定义点击列表项时的回调函数
                      onTap: () {
                        // TODO: 导航到环境搭建教程
                      },
                    ),
                    ListTile(
                      // leading属性设置列表项前面的图标
                      leading: const Icon(Icons.data_object),
                      // title属性设置列表项的标题文本
                      title: Text("左侧导航2"),
                    ),
                    ListTile(
                      // leading属性设置列表项前面的图标
                      leading: const Icon(Icons.storage),
                      // title属性设置列表项的标题文本
                      title: Text("左侧导航3"),
                    ),
                    ListTile(
                      // leading属性设置列表项前面的图标
                      leading: const Icon(Icons.ac_unit_sharp),
                      // title属性设置列表项的标题文本
                      title: Text("左侧导航4"),
                    ),
                    ListTile(
                      // leading属性设置列表项前面的图标
                      leading: const Icon(Icons.access_alarm_outlined),
                      // title属性设置列表项的标题文本
                      title: Text("左侧导航5"),
                    ),
                  ],
                ),
              ),
            ),
            // 另一个Expanded组件，flex值为3，表示占据3份空间（总共4份空间，比例为1:3）
            Expanded(
              flex: 3,
              // Container是一个方便的容器组件
              child: Container(
                // 设置容器背景色为蓝色
                color: Colors.blue,
                // Center组件将其子组件居中显示
                child: Center(child: Text("右侧内容")),
              ),
            ),
          ],
        ),
        // bottomNavigationBar属性定义底部导航栏
        bottomNavigationBar: Container(
          // 设置容器高度为80像素
          height: 80,
          // Center组件将其子组件居中显示
          child: Center(child: Text("这是底部导航")),
        ),
      ),
    ),
  );
}
