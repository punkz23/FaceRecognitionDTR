import 'dart:convert';
import 'dart:io';
import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:facerecognitiondtr/core/api_client.dart';

class AuthRepository {
  final ApiClient _apiClient = ApiClient();

  Future<Map<String, dynamic>> register({
    required String email,
    required String password,
    required String fullName,
    required String employeeId,
    required File imageFile,
  }) async {
    try {
      final bytes = await imageFile.readAsBytes();
      final base64Image = base64Encode(bytes);

      final response = await _apiClient.dio.post(
        'auth/register',
        data: {
          'email': email,
          'password': password,
          'full_name': fullName,
          'employee_id': employeeId,
          'image_base64': base64Image,
        },
      );

      return response.data;
    } catch (e) {
      throw Exception('Registration failed: $e');
    }
  }

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

  Future<Map<String, dynamic>> getUserProfile() async {
    try {
      final response = await _apiClient.dio.get('users/me');
      return response.data;
    } catch (e) {
      throw Exception('Failed to get user profile: $e');
    }
  }
}
