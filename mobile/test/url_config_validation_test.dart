import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:facerecognitiondtr/views/url_config_dialog.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  setUp(() {
    SharedPreferences.setMockInitialValues({});
  });

  testWidgets('UrlConfigDialog shows error for URL:// pattern', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: UrlConfigDialog(),
        ),
      ),
    );

    // Wait for loading to finish
    await tester.pumpAndSettle();

    final textField = find.byType(TextField);
    await tester.enterText(textField, 'URL://192.168.1.100:8000');
    
    final saveButton = find.text('Save');
    await tester.tap(saveButton);
    await tester.pump();

    expect(find.text('Invalid protocol URL:// detected. Use http:// or https://'), findsOneWidget);
  });

  testWidgets('UrlConfigDialog shows error for empty URL', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: UrlConfigDialog(),
        ),
      ),
    );

    await tester.pumpAndSettle();

    final textField = find.byType(TextField);
    await tester.enterText(textField, '');
    
    final saveButton = find.text('Save');
    await tester.tap(saveButton);
    await tester.pump();

    expect(find.text('Please enter a valid URL starting with http/https'), findsOneWidget);
  });
}
