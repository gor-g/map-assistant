import 'package:flutter/material.dart';
import 'screens/homePage.dart';
import 'screens/profilePage.dart';  // Import the user profile page
import 'screens/chatPage.dart';     // Import the empty chat page
import 'package:fac_guide/utils/myColors.dart';


void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      debugShowCheckedModeBanner: false,
      home: HomePage(),
    );
  }
}


