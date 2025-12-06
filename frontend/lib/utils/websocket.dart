import 'package:frontend/models/frame.dart';
import 'package:frontend/providers/audio_providers.dart';
import 'package:frontend/utils/constants.dart';
import 'package:socket_io_client/socket_io_client.dart' as IO;

class Websocket {
  static late IO.Socket socket;

  static void socketConnect() {
    socket = IO.io(socketUrl, <String, dynamic> {
      'transports': ['websocket'],
      'autoConnect': false
    });
    socket.connect();
  }

  static void joinRoom(String roomId) {
    socket.emit('joinRoom', roomId);
  }

  static void leaveRoom(String roomId) {
    socket.emit('leaveRoom', roomId);
  }

  static void receiveFrame(Function(Frame) updateFrame) {
    socket.on('receiveFrame', (data) {
      final dynamic jsonData = Map<String, dynamic>.from(data);
      AudioProviders.audio = jsonData['audio'];
      Frame frame = Frame.fromJson(jsonData);
      updateFrame(frame);
    });
  }
}