import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:dio/dio.dart';
import 'package:facerecognitiondtr/core/api_client.dart';
import 'package:facerecognitiondtr/services/config_service.dart';
import 'package:shared_preferences/shared_preferences.dart';

class MockDio extends Mock implements Dio {}

void main() {
  setUp(() {
    SharedPreferences.setMockInitialValues({});
  });

  test('ApiClient.updateBaseUrl handles trailing slash correctly', () async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('api_base_url', 'http://192.168.1.100:8000/');
    
    final apiClient = ApiClient();
    await apiClient.updateBaseUrl();
    
    expect(apiClient.dio.options.baseUrl, 'http://192.168.1.100:8000/api/v1/');
  });

  test('ApiClient.updateBaseUrl handles missing trailing slash correctly', () async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('api_base_url', 'http://192.168.1.100:8000');
    
    final apiClient = ApiClient();
    await apiClient.updateBaseUrl();
    
    expect(apiClient.dio.options.baseUrl, 'http://192.168.1.100:8000/api/v1/');
  });
}
