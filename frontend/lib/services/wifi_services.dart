import 'dart:convert';
import 'package:frontend/providers/controllers.dart';
import 'package:frontend/utils/constants.dart';
import 'package:http/http.dart';

class WifiServices {
  static Future<void> shareWifiCredentials(String ssid, String password, context) async {
    Map<String, String> body = {
      'ssid' : ssid,
      'pass' : password
    };
    try {
      Response res = await post(
        Uri.parse(wifiUrl),
        headers: apiHeader,
        body: json.encode(body)
      );
      if(res.statusCode == 200) {
        CommonControllers.clearControllers();
      } else {
        print(((json.decode(res.body))['message']).toString());
      }
    } catch(error) {
      print(error.toString());
    }
  }
}