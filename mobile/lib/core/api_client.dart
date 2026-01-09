import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:facerecognitiondtr/core/security_config.dart';

class ApiClient {
  final Dio _dio;
  // Use different URLs for different platforms
  static const String baseUrl = String.fromEnvironment(
    'BASE_URL',
    defaultValue: 'http://localhost:8000/api/v1/',
  );

  ApiClient()
      : _dio = Dio(BaseOptions(
          baseUrl: baseUrl,
          connectTimeout: const Duration(seconds: 10),
          receiveTimeout: const Duration(seconds: 10),
          contentType: 'application/json',
        )) {
    
    // Apply SSL Pinning
    SecurityConfig.setupSslPinning(_dio);

    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        final prefs = await SharedPreferences.getInstance();
        final token = prefs.getString('access_token');
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        return handler.next(options);
      },
      onError: (DioException e, handler) {
        // Handle 401 Unauthorized globally if needed
        return handler.next(e);
      },
    ));
  }

  Dio get dio => _dio;
}
