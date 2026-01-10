import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:facerecognitiondtr/core/api_client.dart';
import 'package:facerecognitiondtr/services/config_service.dart';

class AuthRepository {
  final ApiClient _apiClient;
  final ConfigService _configService;

  AuthRepository({
    ApiClient? apiClient,
    ConfigService? configService,
  })  : _apiClient = apiClient ?? ApiClient(),
        _configService = configService ?? ConfigService();

  Future<void> _updateBaseUrl() async {
    await _apiClient.updateBaseUrl();
  }

  Future<Map<String, dynamic>> register({
    required String email,
    required String password,
    required String fullName,
    required String employeeId,
    required Uint8List imageBytes,
  }) async {
    try {
      print('AuthRepository: Updating base URL...');
      await _updateBaseUrl();
      final baseUrl = _apiClient.dio.options.baseUrl;
      print('AuthRepository: Base URL is $baseUrl');

      print('AuthRepository: Converting image to Base64...');
      final base64Image = base64Encode(imageBytes);
      print('AuthRepository: Base64 length: ${base64Image.length}');

      print('AuthRepository: Sending POST request to auth/register...');
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
      print('AuthRepository: POST request successful. Status: ${response.statusCode}');

      return response.data;
    } on DioException catch (e) {
      final baseUrl = await _configService.getBaseUrl();
      String errorMessage;
      if (e.type == DioExceptionType.connectionTimeout || 
          e.type == DioExceptionType.connectionError) {
        errorMessage = 'Server is unreachable. Please check your connection or backend URL.';
      } else {
        final errorData = e.response?.data;
        errorMessage = errorData != null ? errorData.toString() : e.message ?? 'Unknown error';
      }
      print('Registration Error Details: ${e.response?.data}');
      throw Exception('Registration failed (URL: $baseUrl): $errorMessage');
    } catch (e) {
      final baseUrl = await _configService.getBaseUrl();
      throw Exception('Registration failed (URL: $baseUrl): $e');
    }
  }

  Future<void> login(String email, String password) async {
    try {
      await _updateBaseUrl();
      final response = await _apiClient.dio.post(
        'auth/token',
        data: {'username': email, 'password': password},
        options: Options(contentType: Headers.formUrlEncodedContentType),
      );

      final token = response.data['access_token'];
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('access_token', token);
    } on DioException catch (e) {
      final baseUrl = await _configService.getBaseUrl();
      String errorMessage;
      if (e.type == DioExceptionType.connectionTimeout || 
          e.type == DioExceptionType.connectionError) {
        errorMessage = 'Server is unreachable. Please check your connection or backend URL.';
      } else {
        final errorData = e.response?.data;
        errorMessage = errorData != null ? errorData.toString() : e.message ?? 'Unknown error';
      }
      print('Login Error Details: ${e.response?.data}');
      throw Exception('Login failed (URL: $baseUrl): $errorMessage');
    } catch (e) {
      final baseUrl = await _configService.getBaseUrl();
      throw Exception('Login failed (URL: $baseUrl): $e');
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
      await _updateBaseUrl();
      final response = await _apiClient.dio.get('users/me');
      return response.data;
    } on DioException catch (e) {
      final baseUrl = await _configService.getBaseUrl();
      String errorMessage;
      if (e.type == DioExceptionType.connectionTimeout || 
          e.type == DioExceptionType.connectionError) {
        errorMessage = 'Server is unreachable. Please check your connection or backend URL.';
      } else {
        final errorData = e.response?.data;
        errorMessage = errorData != null ? errorData.toString() : e.message ?? 'Unknown error';
      }
      print('Get User Profile Error Details: ${e.response?.data}');
      throw Exception('Failed to get user profile (URL: $baseUrl): $errorMessage');
    } catch (e) {
      final baseUrl = await _configService.getBaseUrl();
      throw Exception('Failed to get user profile (URL: $baseUrl): $e');
    }
  }
}
