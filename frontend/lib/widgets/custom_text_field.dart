import 'package:flutter/material.dart';
import 'package:frontend/providers/controllers.dart';
import 'package:frontend/utils/colors.dart';
import 'package:frontend/utils/constants.dart';

class CustomTextField extends StatefulWidget {
  final TextInputType keyboardType;
  final TextEditingController controller;
  final String hintText;
  final IconData prefixIcon;
  final bool textObscureNeeded;

  const CustomTextField({super.key,
    required this.keyboardType,
    required this.controller,
    required this.hintText,
    required this.prefixIcon,
    required this.textObscureNeeded
  });

  @override
  State<CustomTextField> createState() => CustomTextFieldState();
}

class CustomTextFieldState extends State<CustomTextField> {
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(defaultPadding),
      child: TextField(
        keyboardType: widget.keyboardType,
        controller: widget.controller,
        obscureText: widget.textObscureNeeded ? CommonControllers.hidePassword : false,
        autofocus: false,
        decoration: InputDecoration(
            enabledBorder: OutlineInputBorder(
                borderSide: BorderSide(
                    color: AppColors.secondaryColor
                ),
                borderRadius: BorderRadius.circular(defaultBorderRadius)
            ),
            focusedBorder: OutlineInputBorder(
                borderSide: BorderSide(
                    color: AppColors.primaryColor,
                    width: 3
                ),
                borderRadius: BorderRadius.circular(defaultBorderRadius)
            ),
            hintText: widget.hintText,
            hintStyle: TextStyle(
                color: AppColors.hintTextColor,
                fontWeight: FontWeight.w400
            ),
            prefixIcon: Icon(
              widget.prefixIcon,
              color: AppColors.primaryColor,
            ),
            suffixIcon: widget.textObscureNeeded ? suffixIcon() : null
        ),
        style: TextStyle(
            color: AppColors.textColor
        ),
      ),
    );
  }

  Widget suffixIcon() {
    return IconButton(
      icon: Icon(
        CommonControllers.hidePassword ? Icons.visibility : Icons.visibility_off,
        color: AppColors.primaryColor,
      ),
      onPressed: () {
        setState(() {
          CommonControllers.hidePassword = !CommonControllers.hidePassword;
        });
      },
    );
  }
}