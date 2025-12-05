import 'package:flutter/material.dart';
import 'package:frontend/utils/colors.dart';
import 'package:frontend/utils/constants.dart';

class Loading extends StatelessWidget {
  const Loading({super.key});

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: Alignment.topCenter,
      child: Container(
        margin: const EdgeInsets.all(defaultMargin),
        height: 50,
        alignment: Alignment.center,
        child: CircularProgressIndicator(
          color: AppColors.primaryColor,
        )
      ),
    );
  }
}