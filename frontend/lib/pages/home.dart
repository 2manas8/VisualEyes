import 'package:flutter/material.dart';
import 'package:frontend/models/frame.dart';
import 'package:frontend/providers/audio_providers.dart';
import 'package:frontend/providers/controllers.dart';
import 'package:frontend/providers/navigation_providers.dart';
import 'package:frontend/services/frame_services.dart';
import 'package:frontend/services/wifi_services.dart';
import 'package:frontend/utils/audio.dart';
import 'package:frontend/utils/colors.dart';
import 'package:frontend/utils/constants.dart';
import 'package:frontend/utils/websocket.dart';
import 'package:frontend/widgets/connect_body.dart';
import 'package:frontend/widgets/custom_navigation_bar.dart';
import 'package:frontend/widgets/custom_title.dart';
import 'package:frontend/widgets/detect_body.dart';
import 'package:frontend/widgets/loading.dart';
import 'package:frontend/widgets/retry_body.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => HomePageState();
}

class HomePageState extends State<HomePage> {
  Frame? frame;
  Audio player = Audio();

  @override
  void initState() {
    super.initState();
    fetchFrame();
    Websocket.socketConnect();
    Websocket.joinRoom('1');
    Websocket.receiveFrame((newFrame) {
      if(NavigationProviders.currentNavigationBarIndex == 1) {
        player.playAudioSequence(AudioProviders.audio);
        setState(() {
          frame = newFrame;
        });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        toolbarHeight: 90,
        backgroundColor: AppColors.baseColor,
        title: CustomTitle(title: NavigationProviders.navigationAppbarTexts[NavigationProviders.currentNavigationBarIndex]),
      ),
      backgroundColor: AppColors.baseColor,
      body: IndexedStack(
        index: NavigationProviders.currentNavigationBarIndex,
        children: [
          ConnectBody(
            onPressedFunction: () async {
              CommonControllers.hidePassword = true;
              await WifiServices.shareWifiCredentials(
                  ConnectControllers.ssidController.text.toString(),
                  ConnectControllers.passwordController.text.toString(),
                  context
              );
              NavigationProviders.currentNavigationBarIndex = 1;
              setState(() {});
              startBackendConnection();
            },
          ),
          FrameControllers.isFetchingFrame
          ? Loading()
          : frame == null
            ? RetryBody(
              onPressedFunction: () {
                fetchFrame();
                Websocket.socketConnect();
                Websocket.joinRoom('1');
              },
            )
            : DetectBody(frame: frame)
        ],
      ),
      bottomNavigationBar: CustomNavigationBar(
        onTapFunction: (index) {
          setState(() {
            NavigationProviders.currentNavigationBarIndex = index;
          });
        },
      ),
    );
  }

  void startBackendConnection() async {
    await Future.delayed(networkSwitchDelay);
    fetchFrame();
    Websocket.socketConnect();
    Websocket.joinRoom('1');
    Websocket.receiveFrame((newFrame) {
      if(NavigationProviders.currentNavigationBarIndex == 1) {
        player.playAudioSequence(AudioProviders.audio);
        setState(() {
          frame = newFrame;
        });
      }
    });
  }

  void fetchFrame() async {
    FrameControllers.isFetchingFrame = true;
    frame = await FrameServices.getLatestFrame('1');
    FrameControllers.isFetchingFrame = false;
    setState(() {});
  }
}