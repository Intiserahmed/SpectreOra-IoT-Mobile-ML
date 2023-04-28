import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'auth_bloc.dart';
import 'my_app.dart';
import 'my_widget.dart';

Future<void> main() async {
  await Supabase.initialize(url: 'SUPABASE_URL', anonKey: 'SUPABASE_ANON_KEY');
  runApp(
    BlocProvider(
      create: (context) => AuthenticationBloc(),
      child: const MyApp(),
    ),
  );
}
