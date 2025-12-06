class Frame {
  String frameUrl;
  String message;

  Frame({
    required this.frameUrl,
    required this.message
  });

  factory Frame.fromJson(Map<String, dynamic> json) {
    return Frame(
      frameUrl: json['frame'],
      message: json['message']
    );
  }
}