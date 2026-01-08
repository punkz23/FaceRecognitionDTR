import 'dart:io';
import 'dart:typed_data';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:dio/dio.dart';
import 'package:facerecognitiondtr/services/attendance_repository.dart';
import 'package:facerecognitiondtr/core/api_client.dart';

class MockApiClient extends Mock implements ApiClient {}
class MockDio extends Mock implements Dio {}
class MockFile extends Mock implements File {}

void main() {
  late AttendanceRepository repository;
  late MockApiClient mockApiClient;
  late MockDio mockDio;

  setUp(() {
    mockApiClient = MockApiClient();
    mockDio = MockDio();
    when(() => mockApiClient.dio).thenReturn(mockDio);
    repository = AttendanceRepository(apiClient: mockApiClient);
  });

  test('clockIn sends correct data and returns response', () async {
    final mockFile = MockFile();
    when(() => mockFile.readAsBytes()).thenAnswer((_) async => Uint8List.fromList([1, 2, 3]));
    
    final responseData = {'id': '123', 'location_verified': true};
    
    when(() => mockDio.post(
      any(),
      data: any(named: 'data'),
    )).thenAnswer((_) async => Response(
      data: responseData,
      statusCode: 200,
      requestOptions: RequestOptions(path: '/attendance/'),
    ));

    final result = await repository.clockIn(mockFile, 14.0, 120.0);

    expect(result, responseData);
    verify(() => mockDio.post(
      '/attendance/',
      data: any(named: 'data'),
    )).called(1);
  });
}