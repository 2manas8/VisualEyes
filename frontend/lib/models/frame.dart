class Frame {
  String frameUrl;
  // List<dynamic> objects;
  String message;

  Frame({
    required this.frameUrl,
    // required this.objects,
    required this.message
  });

  factory Frame.fromJson(Map<String, dynamic> json) {
    return Frame(
      frameUrl: json['frame'],
      // objects: json['objects'],
      message: json['message']
    );
  }
}