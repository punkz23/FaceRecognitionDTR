import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:facerecognitiondtr/views/registration_screen.dart';

void main() {
  testWidgets('RegistrationScreen renders all input fields', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: RegistrationScreen(),
      ),
    );

    expect(find.text('Create Account'), findsOneWidget);
    expect(find.widgetWithText(TextField, 'Full Name'), findsOneWidget);
    expect(find.widgetWithText(TextField, 'Email'), findsOneWidget);
    expect(find.widgetWithText(TextField, 'Employee ID'), findsOneWidget);
    expect(find.widgetWithText(TextField, 'Password'), findsOneWidget);
    expect(find.text('CONTINUE TO FACE CAPTURE'), findsOneWidget);
  });
}
