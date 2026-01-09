import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:facerecognitiondtr/views/login_screen.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:mocktail/mocktail.dart';
import 'package:facerecognitiondtr/logic/auth_bloc/auth_bloc.dart';
import 'package:facerecognitiondtr/services/config_service.dart';
import 'package:shared_preferences/shared_preferences.dart';

class MockAuthBloc extends Mock implements AuthBloc {}

void main() {
  late MockAuthBloc mockAuthBloc;

  setUp(() {
    SharedPreferences.setMockInitialValues({});
    mockAuthBloc = MockAuthBloc();
    when(() => mockAuthBloc.state).thenReturn(AuthInitial());
    when(() => mockAuthBloc.stream).thenAnswer((_) => Stream.fromIterable([AuthInitial()]));
  });

  testWidgets('7 taps on logo opens UrlConfigDialog', (WidgetTester tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: BlocProvider<AuthBloc>.value(
          value: mockAuthBloc,
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
