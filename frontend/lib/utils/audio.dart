import 'dart:convert';
import 'dart:typed_data';
import 'package:audioplayers/audioplayers.dart';

class Audio {
  final AudioPlayer player = AudioPlayer();

  Future<void> playAudioSequence(List<dynamic> base64List) async {
    await player.stop();
    for (String base64String in base64List) {
      try {
        Uint8List audioBytes = base64Decode(base64String);
        await player.play(BytesSource(audioBytes));
        await player.onPlayerComplete.first;
      } catch (e) {
        print("Error playing audio segment: $e");
      }
    }
  }

  void dispose() {
    player.dispose();
  }
}