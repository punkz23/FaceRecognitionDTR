import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:facerecognitiondtr/views/face_enrollment_screen.dart';

void main() {
  testWidgets('FaceEnrollmentScreen shows loading initially', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: FaceEnrollmentScreen(
          email: 'test@example.com',
          password: 'password',
          fullName: 'Test User',
          employeeId: 'EMP123',
        ),
      ),
    );

    expect(find.byType(CircularProgressIndicator), findsOneWidget);
  });
}
