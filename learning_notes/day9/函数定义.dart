// 基本函数
int add(int a, int b) {
  return a + b;
}

// 箭头函数（简洁语法）
int multiply(int a, int b) => a * b;

// 可选参数和非可选参数的主要区别是多了一个大括号和问号，大括号和问号分别表示
String greet(String name, {String? title}) {
  if (title != null) {
    return 'Hello, $title $name!';
  }
  return 'Hello, $name!';
}
/*：
解释这个 Dart 函数中 name 和 title 的区别：
参数类型的区别
String greet(String name, {String? title})
name（位置参数/必需参数）：

没有花括号包裹
必须提供，调用函数时不能省略
类型是 String（非空）
调用时按位置传递
title（命名可选参数）：

用花括号 {} 包裹
可选的，调用时可以不提供
类型是 String?（可空，问号表示可以为 null）
调用时需要指定参数名
*/

// 默认参数值
void printInfo(String name, {int age = 18}) {
  print('$name is $age years old');
}
/*：为什么int可以直接在print中打印，他不是字符串类型

$变量名 语法：会自动调用变量的 .toString() 方法
类型自动转换：
$name → name.toString() → 已经是 String
$age → age.toString() → 将 int 转为 String
*/

void main() {
  print(add(1, 2));
  print(multiply(3, 4));
  print(greet('张三'));
  print(greet('张三', title: 'Mr.'));
  printInfo('张三');
  printInfo('张三', age: 20);
}
