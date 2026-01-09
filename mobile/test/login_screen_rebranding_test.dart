import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:facerecognitiondtr/views/login_screen.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:mocktail/mocktail.dart';
import 'package:facerecognitiondtr/logic/auth_bloc/auth_bloc.dart';

class MockAuthBloc extends Mock implements AuthBloc {}

void main() {
  late MockAuthBloc mockAuthBloc;

  setUp(() {
    mockAuthBloc = MockAuthBloc();
    when(() => mockAuthBloc.state).thenReturn(AuthInitial());
    // Fallback for stream
    when(() => mockAuthBloc.stream).thenAnswer((_) => Stream.fromIterable([AuthInitial()]));
  });

  testWidgets('LoginScreen shows DOFF TimeSafe and new logo', (WidgetTester tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: BlocProvider<AuthBloc>.value(
          value: mockAuthBloc,
          child: const LoginScreen(),
        ),
      ),
    );

    // Verify rebranding text
    expect(find.text('DOFF TimeSafe'), findsOneWidget);
    
    // Verify logo image is used instead of Icon
    expect(find.byType(Image), findsWidgets);
    expect(find.byIcon(Icons.face_retouching_natural), findsNothing);
  });
}
