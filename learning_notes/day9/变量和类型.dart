// 变量声明
var name = '张三';
String title = 'Flutter 教程';
int count = 10;
double price = 99.99;
bool isPublished = true;

// Final 和 Const的区别是，final 和 const 都是只读的，但是 final 是运行时常量，const 是编译时常量。
final DateTime now = DateTime.now(); // 运行时常量
const double pi = 3.14159; // 编译时常量
// 运行时常量和编译时常量的区别在于，final 变量可以在运行时赋值一次，而 const 变量必须在编译时就确定其值。

// 集合类型
List<String> topics = ['环境搭建', '数据模型', '数据库'];
Map<String, dynamic> article = {
  'title': 'Dart 基础',
  'author': '教程作者',
  'views': 1000,
};
void main() {
  print('name: $name');
  print('title: $title');
  print('count: $count');
  print('price: $price');
  print('isPublished: $isPublished');
  print('now: $now');
  print('pi: $pi');
  print(article['title']);
  print(article['author']);
  print(article['views']);
  print(topics[0]);
  print(topics);
  print(article);
  print(topics.length);
  print(article.keys);
  print(article.values);
  print(article.containsKey('title'));
  print(article.containsValue('Dart 教程'));
  print(article.remove('title'));
  print(article);
  topics.add('路由');
  print(topics);
  topics.remove('环境搭建');
}
