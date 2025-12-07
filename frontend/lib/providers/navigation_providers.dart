import 'package:flutter/material.dart';
import 'package:frontend/utils/constants.dart';

class NavigationProviders {
  static int currentNavigationBarIndex = 0;

  static List<BottomNavigationBarItem> items = [
    BottomNavigationBarItem(
      icon: Icon(
        Icons.wifi
      ),
      label: connectText
    ),
    BottomNavigationBarItem(
      icon: Icon(
        Icons.remove_red_eye_outlined
      ),
      label: detectText
    )
  ];

  static List<String> navigationAppbarTexts = [
    connectText,
    detectText
  ];
}