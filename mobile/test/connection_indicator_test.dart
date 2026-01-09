import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:facerecognitiondtr/views/login_screen.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:mocktail/mocktail.dart';
import 'package:facerecognitiondtr/logic/auth_bloc/auth_bloc.dart';
import 'package:facerecognitiondtr/logic/connectivity_bloc/connectivity_bloc.dart';
import 'package:facerecognitiondtr/logic/connectivity_bloc/connectivity_event.dart';
import 'package:facerecognitiondtr/logic/connectivity_bloc/connectivity_state.dart';

class MockAuthBloc extends Mock implements AuthBloc {}
class MockConnectivityBloc extends Mock implements ConnectivityBloc {}

void main() {
  late MockAuthBloc mockAuthBloc;
  late MockConnectivityBloc mockConnectivityBloc;

  setUp(() {
    mockAuthBloc = MockAuthBloc();
    mockConnectivityBloc = MockConnectivityBloc();
    
    when(() => mockAuthBloc.state).thenReturn(AuthInitial());
    when(() => mockAuthBloc.stream).thenAnswer((_) => Stream.fromIterable([AuthInitial()]));
  });

  testWidgets('Login button is disabled when offline', (WidgetTester tester) async {
    when(() => mockConnectivityBloc.state).thenReturn(ConnectivityOffline());
    when(() => mockConnectivityBloc.stream).thenAnswer((_) => Stream.fromIterable([ConnectivityOffline()]));

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

    final loginButton = tester.widget<ElevatedButton>(find.byType(ElevatedButton));
    expect(loginButton.onPressed, isNull);
    expect(find.text('Offline'), findsOneWidget);
  });

  testWidgets('Login button is enabled when online', (WidgetTester tester) async {
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

    final loginButton = tester.widget<ElevatedButton>(find.byType(ElevatedButton));
    expect(loginButton.onPressed, isNotNull);
    expect(find.text('Online'), findsOneWidget);
  });
}
