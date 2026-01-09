import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:facerecognitiondtr/core/api_client.dart';

class AuthRepository {
  final ApiClient _apiClient = ApiClient();

  Future<void> login(String email, String password) async {
    try {
      final response = await _apiClient.dio.post(
        'auth/token',
        data: {'username': email, 'password': password},
        options: Options(contentType: Headers.formUrlEncodedContentType),
      );

      final token = response.data['access_token'];
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('access_token', token);
    } catch (e) {
      throw Exception('Login failed: $e');
    }
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('access_token');
  }

  Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('access_token');
  }
}
