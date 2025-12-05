import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:frontend/models/frame.dart';
import 'package:frontend/providers/controllers.dart';
import 'package:frontend/services/frame_services.dart';
import 'package:frontend/utils/colors.dart';
import 'package:frontend/utils/constants.dart';
import 'package:frontend/widgets/action_button.dart';
import 'package:frontend/widgets/custom_title.dart';
import 'package:frontend/widgets/loading.dart';

class DetectPage extends StatefulWidget {
  const DetectPage({super.key});

  @override
  State<DetectPage> createState() => DetectPageState();
}

class DetectPageState extends State<DetectPage> {
  Frame? frame;

  @override
  void initState() {
    super.initState();
    fetchFrame();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        toolbarHeight: 90,
        backgroundColor: AppColors.baseColor,
        // actions: [
        //   ActionButton(
        //     onPressedFunction: () {
        //       print('Logout');
        //     },
        //     icon: Icons.logout
        //   )
        // ],
        title: const CustomTitle(title: detectText),
      ),
      backgroundColor: AppColors.baseColor,
      body: FrameControllers.isFetchingFrame
      ? Loading()
      : Center(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(defaultPadding),
              child: SizedBox(
                width: 350,
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(defaultBorderRadius),
                  child: Image.memory(base64Decode(frame!.frameUrl))
                ),
              ),
            ),
            SizedBox(height: 30),
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
                        frame!.message,
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
      ),
    );
  }

  void fetchFrame() async {
    FrameControllers.isFetchingFrame = true;
    frame = await FrameServices.getLatestFrame('1');
    FrameControllers.isFetchingFrame = false;
    setState(() {});
  }
}