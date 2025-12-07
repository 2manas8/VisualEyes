import 'package:flutter/material.dart';
import 'package:frontend/utils/colors.dart';
import 'package:frontend/utils/constants.dart';

class ClickButton extends StatefulWidget {
  final String text;
  final void Function() onPressedFunction;

  const ClickButton({super.key,
    required this.text,
    required this.onPressedFunction
  });

  @override
  State<ClickButton> createState() => ClickButtonState();
}

class ClickButtonState extends State<ClickButton> {
  @override
  Widget build(BuildContext context) {
    return Container(
      width: 110,
      margin: const EdgeInsets.all(defaultMargin),
      child: ElevatedButton(
        onPressed: widget.onPressedFunction,
        style: ButtonStyle(
            backgroundColor: WidgetStateProperty.all(AppColors.primaryColor)
        ),
        child: Center(
          child: Text(
            widget.text,
            style: TextStyle(
                color: AppColors.baseColor,
                fontWeight: FontWeight.bold
            ),
          ),
        ),
      ),
    );
  }
}