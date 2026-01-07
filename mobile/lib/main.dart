import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:facerecognitiondtr/views/login_screen.dart';
import 'package:facerecognitiondtr/views/dashboard_screen.dart';
import 'package:facerecognitiondtr/logic/auth_bloc/auth_bloc.dart';
import 'package:facerecognitiondtr/services/auth_repository.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  print('Starting SafeTime DTR app...');
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: [
        BlocProvider(
          create: (context) => AuthBloc(authRepository: AuthRepository())..add(AppStarted()),
        ),
      ],
      child: MaterialApp(
        title: 'SafeTime DTR',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          useMaterial3: true,
          colorScheme: ColorScheme.fromSeed(
            seedColor: const Color(0xFF0D47A1),
            primary: const Color(0xFF0D47A1),
          ),
        ),
        home: BlocBuilder<AuthBloc, AuthState>(
          builder: (context, state) {
            print('Current auth state: ${state.runtimeType}');
            if (state is AuthAuthenticated) {
              return const DashboardScreen();
            }
            return const LoginScreen();
          },
        ),
      ),
    );
  }
}
