import 'package:flutter/material.dart';
import 'package:frontend/providers/navigation_providers.dart';
import 'package:frontend/utils/colors.dart';

class CustomNavigationBar extends StatefulWidget {
  final void Function(int) onTapFunction;

  const CustomNavigationBar({
    required this.onTapFunction
  });

  @override
  State<CustomNavigationBar> createState() => CustomNavigationBarState();
}

class CustomNavigationBarState extends State<CustomNavigationBar> {
  @override
  Widget build(BuildContext context) {
    return BottomNavigationBar(
      type: BottomNavigationBarType.fixed,
      selectedItemColor: AppColors.primaryColor,
      unselectedItemColor: AppColors.secondaryColor,
      backgroundColor: AppColors.baseColor,
      elevation: 0,
      currentIndex: NavigationProviders.currentNavigationBarIndex,
      onTap: widget.onTapFunction,
      items: NavigationProviders.items,
    );
  }
}