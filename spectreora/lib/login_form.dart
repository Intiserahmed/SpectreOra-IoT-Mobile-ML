import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'auth_bloc.dart';

class LoginForm extends StatefulWidget {
  const LoginForm({Key? key}) : super(key: key);

  @override
  State<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  bool _isLoading = false;
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  Future<void> _signIn(BuildContext context) async {
    if (_formKey.currentState!.validate()) {
      setState(() => _isLoading = true);

      final response = await Supabase.instance.client.auth.signIn(
        email: _emailController.text,
        password: _passwordController.text,
      );

      if (response.error == null) {
        BlocProvider.of<AuthenticationBloc>(context)
            .add(AuthenticationEvent.loggedIn);
      } else {
        ScaffoldMessenger.of(context)
            .showSnackBar(SnackBar(content: Text(response.error!.message)));
      }

      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Center(
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(32.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                TextFormField(
                  controller: _emailController,
                  keyboardType: TextInputType.emailAddress,
                  decoration: const InputDecoration(
                    labelText: 'Email',
                  ),
                  validator: (value) =>
                      value!.isEmpty ? 'Please enter an email' : null,
                ),
                TextFormField(
                  controller: _passwordController,
                  obscureText: true,
                  decoration: const InputDecoration(
                    labelText: 'Password',
                  ),
                  validator: (value) =>
                      value!.isEmpty ? 'Please enter a password' : null,
                ),
                const SizedBox(height: 16),
                _isLoading
                    ? const CircularProgressIndicator()
                    : ElevatedButton(
                        onPressed: () => _signIn(context),
                        child: const Text('Sign In'),
                      ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
