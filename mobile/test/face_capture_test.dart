import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:facerecognitiondtr/views/face_capture_screen.dart';

void main() {
  testWidgets('FaceCaptureScreen shows loading initially', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: FaceCaptureScreen(),
      ),
    );

    // Should show loading while camera is initializing
    expect(find.byType(CircularProgressIndicator), findsOneWidget);
  });
}
