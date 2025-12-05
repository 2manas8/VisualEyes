import 'package:flutter/material.dart';
import 'package:frontend/utils/constants.dart';

class SplashScreenImage extends StatelessWidget {
  const SplashScreenImage({super.key});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: SizedBox(
        height: 300,
        width: 300,
        child: Image.asset(logo),
      )
    );
  }
}