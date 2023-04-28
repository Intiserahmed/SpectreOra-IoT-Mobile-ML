import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'auth_bloc.dart';
import 'home_page.dart';
import 'login_form.dart';

class MyWidget extends StatelessWidget {
  const MyWidget({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Login Example'),
      ),
      body: BlocBuilder<AuthenticationBloc, User?>(
        builder: (context, user) {
          return user == null ? const LoginForm() : const SignOutPage();
        },
      ),
    );
  }
}
