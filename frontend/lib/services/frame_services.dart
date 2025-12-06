import 'dart:convert';
import 'package:frontend/models/frame.dart';
import 'package:frontend/utils/constants.dart';
import 'package:http/http.dart';

class FrameServices {
  static Future<Frame?> getLatestFrame(String roomId) async{
    try {
      Response res = await get(Uri.parse(apiBaseUrl + latestFrameEndpoint).replace(queryParameters: {'roomId': roomId}));
      if(res.statusCode == 200) {
        final dynamic jsonData = json.decode(res.body);
        return Frame.fromJson(jsonData);
      }
    } catch(error) {
      print(error.toString());
    }
    return null;
  }
}