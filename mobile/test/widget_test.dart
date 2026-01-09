import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:mocktail/mocktail.dart';
import 'package:facerecognitiondtr/views/login_screen.dart';
import 'package:facerecognitiondtr/logic/auth_bloc/auth_bloc.dart';
import 'package:facerecognitiondtr/logic/connectivity_bloc/connectivity_bloc.dart';
import 'package:facerecognitiondtr/logic/connectivity_bloc/connectivity_state.dart';

class MockAuthBloc extends Mock implements AuthBloc {}
class MockConnectivityBloc extends Mock implements ConnectivityBloc {}

void main() {
  testWidgets('LoginScreen renders email and password fields', (WidgetTester tester) async {
    final mockAuthBloc = MockAuthBloc();
    final mockConnectivityBloc = MockConnectivityBloc();

    when(() => mockAuthBloc.state).thenReturn(AuthInitial());
    when(() => mockAuthBloc.stream).thenAnswer((_) => Stream.fromIterable([AuthInitial()]));

    when(() => mockConnectivityBloc.state).thenReturn(ConnectivityOnline());
    when(() => mockConnectivityBloc.stream).thenAnswer((_) => Stream.fromIterable([ConnectivityOnline()]));

    await tester.pumpWidget(
      MaterialApp(
        home: MultiBlocProvider(
          providers: [
            BlocProvider<AuthBloc>.value(value: mockAuthBloc),
            BlocProvider<ConnectivityBloc>.value(value: mockConnectivityBloc),
          ],
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