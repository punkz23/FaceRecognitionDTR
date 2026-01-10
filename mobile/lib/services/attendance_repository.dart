import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'package:facerecognitiondtr/core/api_client.dart';

class AttendanceRepository {
  final ApiClient _apiClient;

  AttendanceRepository({ApiClient? apiClient}) : _apiClient = apiClient ?? ApiClient();

  Future<void> _updateBaseUrl() async {
    await _apiClient.updateBaseUrl();
  }

  Future<Map<String, dynamic>> clockIn(Uint8List imageBytes, double? lat, double? long) async {
    try {
      await _updateBaseUrl();
      final base64Image = base64Encode(imageBytes);

      final response = await _apiClient.dio.post('attendance/', data: {
        'snapshot_base64': base64Image,
        'type': 'CLOCK_IN',
        'latitude': lat,
        'longitude': long,
      });

      return response.data;
    } catch (e) {
      throw Exception('Clock-in failed: $e');
    }
  }

  Future<List<dynamic>> getHistory() async {
    try {
      await _updateBaseUrl();
      final response = await _apiClient.dio.get('attendance/history');
      return response.data;
    } catch (e) {
      throw Exception('Failed to fetch history: $e');
    }
  }
}