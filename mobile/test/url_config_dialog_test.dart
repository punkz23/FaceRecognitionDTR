import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:facerecognitiondtr/views/login_screen.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:mocktail/mocktail.dart';
import 'package:facerecognitiondtr/logic/auth_bloc/auth_bloc.dart';
import 'package:facerecognitiondtr/logic/connectivity_bloc/connectivity_bloc.dart';
import 'package:facerecognitiondtr/logic/connectivity_bloc/connectivity_state.dart';
import 'package:facerecognitiondtr/services/config_service.dart';
import 'package:shared_preferences/shared_preferences.dart';

class MockAuthBloc extends Mock implements AuthBloc {}
class MockConnectivityBloc extends Mock implements ConnectivityBloc {}

void main() {
  late MockAuthBloc mockAuthBloc;
  late MockConnectivityBloc mockConnectivityBloc;

  setUp(() {
    SharedPreferences.setMockInitialValues({});
    mockAuthBloc = MockAuthBloc();
    mockConnectivityBloc = MockConnectivityBloc();

    when(() => mockAuthBloc.state).thenReturn(AuthInitial());
    when(() => mockAuthBloc.stream).thenAnswer((_) => Stream.fromIterable([AuthInitial()]));

    when(() => mockConnectivityBloc.state).thenReturn(ConnectivityOnline());
    when(() => mockConnectivityBloc.stream).thenAnswer((_) => Stream.fromIterable([ConnectivityOnline()]));
  });

  testWidgets('7 taps on logo opens UrlConfigDialog', (WidgetTester tester) async {
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

    final logoFinder = find.byType(Image);
    expect(logoFinder, findsOneWidget);

    for (int i = 0; i < 7; i++) {
      await tester.tap(logoFinder);
    }
    await tester.pumpAndSettle();

    expect(find.text('Backend Configuration'), findsOneWidget);
    expect(find.widgetWithText(TextField, 'API Base URL'), findsOneWidget);
  });
}
