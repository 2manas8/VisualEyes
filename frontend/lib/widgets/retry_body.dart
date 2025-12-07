import 'package:flutter/material.dart';
import 'package:frontend/utils/colors.dart';
import 'package:frontend/utils/constants.dart';
import 'package:frontend/widgets/click_button.dart';

class RetryBody extends StatefulWidget {
  final void Function() onPressedFunction;

  const RetryBody({
    required this.onPressedFunction
  });

  @override
  State<RetryBody> createState() => RetryBodyState();
}

class RetryBodyState extends State<RetryBody> {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.router, size: 50, color: AppColors.textColor),
          SizedBox(height: 20),
          Text("Connecting to server...", style: TextStyle(color: AppColors.textColor)),
          SizedBox(height: 20),
          ClickButton(
            text: retryText,
            onPressedFunction: widget.onPressedFunction
          )
        ],
      ),
    );
  }
}