import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:facerecognitiondtr/views/login_screen.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:mocktail/mocktail.dart';
import 'package:facerecognitiondtr/logic/auth_bloc/auth_bloc.dart';
import 'package:facerecognitiondtr/logic/connectivity_bloc/connectivity_bloc.dart';
import 'package:facerecognitiondtr/logic/connectivity_bloc/connectivity_state.dart';

class MockAuthBloc extends Mock implements AuthBloc {}
class MockConnectivityBloc extends Mock implements ConnectivityBloc {}

void main() {
  late MockAuthBloc mockAuthBloc;
  late MockConnectivityBloc mockConnectivityBloc;
  late StreamController<AuthState> authStateController;

  setUp(() {
    mockAuthBloc = MockAuthBloc();
    mockConnectivityBloc = MockConnectivityBloc();
    authStateController = StreamController<AuthState>.broadcast();

    when(() => mockAuthBloc.state).thenReturn(AuthInitial());
    when(() => mockAuthBloc.stream).thenAnswer((_) => authStateController.stream);

    when(() => mockConnectivityBloc.state).thenReturn(ConnectivityOnline());
    when(() => mockConnectivityBloc.stream).thenAnswer((_) => Stream.fromIterable([ConnectivityOnline()]));
  });

  tearDown(() {
    authStateController.close();
  });

  testWidgets('LoginScreen dismisses loading indicator on AuthFailure', (WidgetTester tester) async {
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

    expect(find.text('LOGIN'), findsOneWidget);
    expect(find.byType(CircularProgressIndicator), findsNothing);

    // Simulate AuthLoading
    when(() => mockAuthBloc.state).thenReturn(AuthLoading());
    authStateController.add(AuthLoading());
    await tester.pump(); // Start the animation/rebuild

    expect(find.byType(CircularProgressIndicator), findsOneWidget);
    expect(find.text('LOGIN'), findsNothing);

    // Simulate AuthFailure
    when(() => mockAuthBloc.state).thenReturn(AuthFailure('Error 400'));
    authStateController.add(AuthFailure('Error 400'));
    await tester.pump(); // Trigger rebuild for state change

    expect(find.byType(CircularProgressIndicator), findsNothing);
    expect(find.text('LOGIN'), findsOneWidget);
    
    // Verify SnackBar shown
    await tester.pumpAndSettle(); // Wait for SnackBar animation
    expect(find.text('Error 400'), findsOneWidget);
  });
}