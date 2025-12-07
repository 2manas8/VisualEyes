import 'package:flutter/material.dart';
import 'package:frontend/providers/controllers.dart';
import 'package:frontend/utils/constants.dart';
import 'package:frontend/widgets/click_button.dart';
import 'package:frontend/widgets/custom_text_field.dart';

class ConnectBody extends StatefulWidget {
  final void Function() onPressedFunction;

  const ConnectBody({
    required this.onPressedFunction
  });

  @override
  State<ConnectBody> createState() => ConnectBodyState();
}

class ConnectBodyState extends State<ConnectBody> {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        children: [
          SizedBox(height: 100),
          CustomTextField(
            keyboardType: TextInputType.text,
            controller: ConnectControllers.ssidController,
            hintText: wifiSsidText,
            prefixIcon: Icons.account_circle,
            textObscureNeeded: false
          ),
          CustomTextField(
            keyboardType: TextInputType.text,
            controller: ConnectControllers.passwordController,
            hintText: wifiPasswordText,
            prefixIcon: Icons.key,
            textObscureNeeded: true
          ),
          ClickButton(
            text: connectText,
            onPressedFunction: widget.onPressedFunction
          )
        ],
      ),
    );
  }
}