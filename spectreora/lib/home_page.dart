import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'auth_bloc.dart';

class SignOutPage extends StatelessWidget {
  const SignOutPage({Key? key}) : super(key: key);

  Future<void> _signOut(BuildContext context) async {
    await Supabase.instance.client.auth.signOut();
    BlocProvider.of<AuthenticationBloc>(context)
        .add(AuthenticationEvent.loggedOut);
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Text('Signed In'),
          ElevatedButton(
            onPressed: () => _signOut(context),
            child: const Text('Sign Out'),
          ),
        ],
      ),
    );
  }
}
