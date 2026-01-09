import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:facerecognitiondtr/core/security_config.dart';
import 'package:facerecognitiondtr/services/config_service.dart';

class ApiClient {
  final Dio _dio;
  final ConfigService _configService = ConfigService();
  
  // Use different URLs for different platforms
  static const String defaultBaseUrl = String.fromEnvironment(
    'BASE_URL',
    defaultValue: 'http://localhost:8000',
  );

  ApiClient()
      : _dio = Dio(BaseOptions(
          baseUrl: '$defaultBaseUrl/api/v1/',
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

  Future<void> updateBaseUrl() async {
    final baseUrl = await _configService.getBaseUrl();
    // Ensure robust joining: remove trailing slashes from base and add /api/v1/
    String sanitizedBase = baseUrl.endsWith('/') 
        ? baseUrl.substring(0, baseUrl.length - 1) 
        : baseUrl;
    _dio.options.baseUrl = '$sanitizedBase/api/v1/';
  }

  Dio get dio => _dio;
}
