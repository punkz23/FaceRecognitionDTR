import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:facerecognitiondtr/views/login_screen.dart';
import 'package:facerecognitiondtr/logic/auth_bloc/auth_bloc.dart';
import 'package:facerecognitiondtr/services/auth_repository.dart';

void main() {
  testWidgets('LoginScreen renders email and password fields', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    // We need to provide the AuthBloc
    await tester.pumpWidget(
      MaterialApp(
        home: BlocProvider(
          create: (context) => AuthBloc(authRepository: AuthRepository()),
          child: const LoginScreen(),
        ),
      ),
    );

    // Verify that our app name is displayed.
    expect(find.text('DOFF TimeSafe'), findsOneWidget);

    // Verify that email and password fields are present
    expect(find.text('Email'), findsOneWidget);
    expect(find.text('Password'), findsOneWidget);

    // Verify Login button exists
    expect(find.text('LOGIN'), findsOneWidget);
  });
}
