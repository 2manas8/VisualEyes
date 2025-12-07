import 'package:flutter/material.dart';

class FrameControllers {
  static bool isFetchingFrame = false;
}

class ConnectControllers {
  static TextEditingController ssidController = TextEditingController();
  static TextEditingController passwordController = TextEditingController();
}

class CommonControllers {
  static bool hidePassword = true;

  static void clearControllers() {
    ConnectControllers.ssidController.clear();
    ConnectControllers.passwordController.clear();
  }
}