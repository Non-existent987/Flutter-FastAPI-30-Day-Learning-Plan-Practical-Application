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
