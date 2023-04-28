import 'package:flutter/material.dart';
import 'my_widget.dart';

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Supabase Flutter Demo',
      home: const MyWidget(),
    );
  }
}
