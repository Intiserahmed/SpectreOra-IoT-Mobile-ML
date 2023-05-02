import 'package:go_router/go_router.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:spectreora_app/ecg/view/ecg_page.dart';

import '../auth/view/login_page.dart';
import '../onboarding/view/verification_page.dart';

part 'routes.g.dart';

@riverpod
route(RouteRef _) => _routes;

final _routes = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomePage(),
    ),
    GoRoute(
      path: '/login',
      builder: (context, state) => const LoginPage(),
    ),
    GoRoute(
      path: '/verification',
      builder: (context, state) {
        final params = state.extra as VerificationPageParams?;

        if (params == null) {
          throw 'Missing `VerificationPageParams` object';
        }

        return VerificationPage(params: params);
      },
    ),
  ],
);
