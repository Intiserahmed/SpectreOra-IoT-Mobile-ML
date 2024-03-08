import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

import 'core/routes.dart';

Future<void> main() async {
  await dotenv.load(fileName: ".env");
  String? supabase_url = dotenv.env['SUPABASE_URL'];
  String? supabase_apikey = dotenv.env['SUPABASE_KEY'];

  await Supabase.initialize(
    url: supabase_url!,
    anonKey: supabase_apikey!,
  );

  runApp(const ProviderScope(child: MyApp()));
}

class MyApp extends ConsumerWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final routes = ref.read(routeProvider);
    return MaterialApp.router(
      title: 'SpectreOra',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blueGrey,
      ),
      routerConfig: routes,
    );
  }
}
