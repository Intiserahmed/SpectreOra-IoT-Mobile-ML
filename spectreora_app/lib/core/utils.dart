import 'package:flutter/material.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'utils.g.dart';

extension BuildContextExt on BuildContext {
  ScaffoldFeatureController<SnackBar, SnackBarClosedReason> showAlert(
    String message,
  ) =>
      ScaffoldMessenger.of(this).showSnackBar(
        SnackBar(
          content: Text(message),
          duration: const Duration(milliseconds: 2000),
        ),
      );

  Future<T?> showBottomSheet<T>({
    required Widget child,
  }) =>
      showModalBottomSheet<T>(
        context: this,
        builder: (_) => child,
      );
}
