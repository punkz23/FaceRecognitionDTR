import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:mocktail/mocktail.dart';
import 'package:facerecognitiondtr/views/dashboard_screen.dart';
import 'package:facerecognitiondtr/logic/auth_bloc/auth_bloc.dart';
import 'package:facerecognitiondtr/services/auth_repository.dart';

class MockAuthRepository extends Mock implements AuthRepository {}

void main() {
  late AuthBloc authBloc;
  late MockAuthRepository mockAuthRepository;

  setUp(() {
    mockAuthRepository = MockAuthRepository();
    authBloc = AuthBloc(authRepository: mockAuthRepository);
  });

  tearDown(() {
    authBloc.close();
  });

  testWidgets('DashboardScreen shows pending warning and disables button', (WidgetTester tester) async {
    final pendingUser = {
      'id': 'uuid',
      'email': 'pending@example.com',
      'status': 'PENDING',
      'full_name': 'Pending User'
    };

    await tester.pumpWidget(
      MaterialApp(
        home: BlocProvider<AuthBloc>.value(
          value: authBloc,
          child: const DashboardScreen(),
        ),
      ),
    );

    // Initial state is AuthInitial, so we manually emit Authenticated with PENDING
    authBloc.emit(AuthAuthenticated(pendingUser));
    await tester.pumpAndSettle();

    expect(find.textContaining('pending approval'), findsOneWidget);
    
    final timeInButton = tester.widget<ElevatedButton>(find.byType(ElevatedButton));
    expect(timeInButton.onPressed, isNull); // Disabled
  });

  testWidgets('DashboardScreen enables button for APPROVED users', (WidgetTester tester) async {
    final approvedUser = {
      'id': 'uuid',
      'email': 'approved@example.com',
      'status': 'APPROVED',
      'full_name': 'Approved User'
    };

    await tester.pumpWidget(
      MaterialApp(
        home: BlocProvider<AuthBloc>.value(
          value: authBloc,
          child: const DashboardScreen(),
        ),
      ),
    );

    authBloc.emit(AuthAuthenticated(approvedUser));
    await tester.pumpAndSettle();

    expect(find.textContaining('pending approval'), findsNothing);
    
    final timeInButton = tester.widget<ElevatedButton>(find.byType(ElevatedButton));
    expect(timeInButton.onPressed, isNotNull); // Enabled
  });
}
