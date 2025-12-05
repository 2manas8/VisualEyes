import 'package:flutter/material.dart';
import 'package:frontend/utils/colors.dart';
import 'package:frontend/utils/constants.dart';

class CustomTitle extends StatelessWidget {
  final String title;

  const CustomTitle({
    super.key,
    required this.title
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(defaultPadding),
      child: Text(
        detectText,
        style: TextStyle(
          color: AppColors.primaryColor,
          fontWeight: FontWeight.bold,
          fontSize: 40
        ),
      ),
    );
  }
}