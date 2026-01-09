import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:facerecognitiondtr/logic/auth_bloc/auth_bloc.dart';
import 'package:facerecognitiondtr/logic/connectivity_bloc/connectivity_bloc.dart';
import 'package:facerecognitiondtr/logic/connectivity_bloc/connectivity_event.dart';
import 'package:facerecognitiondtr/logic/connectivity_bloc/connectivity_state.dart';
import 'package:facerecognitiondtr/views/registration_screen.dart';
import 'package:facerecognitiondtr/views/url_config_dialog.dart';
import 'dart:async';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  int _logoTapCount = 0;
  Timer? _connectivityTimer;

  @override
  void initState() {
    super.initState();
    // Initial check
    context.read<ConnectivityBloc>().add(CheckConnectivity());
    // Periodic check every 30 seconds
    _connectivityTimer = Timer.periodic(const Duration(seconds: 30), (timer) {
      if (mounted) {
        context.read<ConnectivityBloc>().add(CheckConnectivity());
      }
    });
  }

  @override
  void dispose() {
    _connectivityTimer?.cancel();
    super.dispose();
  }

  void _onLogoTap() {
    _logoTapCount++;
    if (_logoTapCount >= 7) {
      _logoTapCount = 0;
      showDialog<bool>(
        context: context,
        builder: (context) => const UrlConfigDialog(),
      ).then((updated) {
        if (updated == true) {
          context.read<ConnectivityBloc>().add(CheckConnectivity());
        }
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: BlocListener<AuthBloc, AuthState>(
        listener: (context, state) {
          if (state is AuthFailure) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text(state.error), backgroundColor: Colors.red),
            );
          }
        },
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                GestureDetector(
                  onTap: _onLogoTap,
                  child: Image.asset(
                    'assets/logo.png',
                    height: 100,
                  ),
                ),
                const SizedBox(height: 24),
                const Text(
                  'DOFF TimeSafe',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF0D47A1),
                  ),
                ),
                const SizedBox(height: 48),
                TextField(
                  controller: _emailController,
                  decoration: const InputDecoration(
                    labelText: 'Email',
                    prefixIcon: Icon(Icons.email_outlined),
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 16),
                TextField(
                  controller: _passwordController,
                  obscureText: true,
                  decoration: const InputDecoration(
                    labelText: 'Password',
                    prefixIcon: Icon(Icons.lock_outline),
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 24),
                BlocBuilder<AuthBloc, AuthState>(
                  builder: (context, authState) {
                    return BlocBuilder<ConnectivityBloc, ConnectivityState>(
                      builder: (context, connectivityState) {
                        final isOnline = connectivityState is ConnectivityOnline;
                        final isLoading = authState is AuthLoading;

                        if (authState is AuthLoading) {
                          return const Center(child: CircularProgressIndicator());
                        }

                        return ElevatedButton(
                          onPressed: isOnline
                              ? () {
                                  print('Login button pressed with email: ${_emailController.text}');
                                  context.read<AuthBloc>().add(
                                        LoginRequested(
                                          _emailController.text,
                                          _passwordController.text,
                                        ),
                                      );
                                }
                              : null,
                          style: ElevatedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 16),
                            backgroundColor: const Color(0xFF0D47A1),
                            foregroundColor: Colors.white,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                          ),
                          child: const Text(
                            'LOGIN',
                            style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                          ),
                        );
                      },
                    );
                  },
                ),
                const SizedBox(height: 16),
                BlocBuilder<ConnectivityBloc, ConnectivityState>(
                  builder: (context, state) {
                    Color color = Colors.grey;
                    String text = 'Checking connection...';

                    if (state is ConnectivityOnline) {
                      color = Colors.green;
                      text = 'Online';
                    } else if (state is ConnectivityOffline) {
                      color = Colors.red;
                      text = 'Offline';
                    }

                    return Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Container(
                          width: 10,
                          height: 10,
                          decoration: BoxDecoration(
                            color: color,
                            shape: BoxShape.circle,
                          ),
                        ),
                        const SizedBox(width: 8),
                        Text(
                          text,
                          style: TextStyle(
                            color: color,
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    );
                  },
                ),
                const SizedBox(height: 16),
                TextButton(
                  onPressed: () {
                    Navigator.of(context).push(
                      MaterialPageRoute(builder: (context) => const RegistrationScreen()),
                    );
                  },
                  child: const Text('New employee? REGISTER'),
                ),
                TextButton(
                  onPressed: () {},
                  child: const Text('Forgot Password?'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
