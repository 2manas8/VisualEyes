import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:frontend/models/frame.dart';
import 'package:frontend/utils/colors.dart';
import 'package:frontend/utils/constants.dart';

class DetectBody extends StatefulWidget {
  final Frame? frame;

  const DetectBody({
    required this.frame
  });

  @override
  State<DetectBody> createState() => DetectBodyState();
}

class DetectBodyState extends State<DetectBody> {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        children: [
          SizedBox(height: 50),
          Padding(
            padding: const EdgeInsets.all(defaultPadding),
            child: SizedBox(
              width: 350,
              child: ClipRRect(
                borderRadius: BorderRadius.circular(defaultBorderRadius),
                child: Image.memory(base64Decode(widget.frame!.frameUrl))
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(defaultPadding),
            child: Container(
              width: 350,
              decoration: BoxDecoration(
                  color: AppColors.secondaryColor,
                  borderRadius: BorderRadius.circular(defaultBorderRadius),
                  border: Border.all(
                      color: AppColors.primaryColor
                  )
              ),
              child: Container(
                margin: const EdgeInsets.all(defaultMargin),
                padding: const EdgeInsets.all(defaultPadding),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      descriptionText,
                      style: TextStyle(
                        color: AppColors.textColor,
                        fontWeight: FontWeight.bold
                      )
                    ),
                    Text(
                      widget.frame!.message,
                      style: TextStyle(
                        color: AppColors.textColor
                      ),
                    )
                  ],
                ),
              ),
            ),
          )
        ],
      ),
    );
  }
}