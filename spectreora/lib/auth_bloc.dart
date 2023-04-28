import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

enum AuthenticationEvent { check, loggedIn, loggedOut }

class AuthenticationBloc extends Bloc<AuthenticationEvent, User?> {
  AuthenticationBloc() : super(null) {
    Supabase.instance.client.auth.onAuthStateChange.listen((data) {
      add(data.event == AuthEventTypes.signedIn
          ? AuthenticationEvent.loggedIn
          : AuthenticationEvent.loggedOut);
    });
    add(AuthenticationEvent.check);
  }

  @override
  Stream<User?> mapEventToState(AuthenticationEvent event) async* {
    switch (event) {
      case AuthenticationEvent.check:
        yield Supabase.instance.client.auth.currentUser;
        break;
      case AuthenticationEvent.loggedIn:
        yield Supabase.instance.client.auth.currentUser;
        break;
      case AuthenticationEvent.loggedOut:
        yield null;
        break;
    }
  }
}
