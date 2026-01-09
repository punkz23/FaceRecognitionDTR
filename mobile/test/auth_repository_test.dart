import 'dart:io';
import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:dio/dio.dart';
import 'package:facerecognitiondtr/services/auth_repository.dart';
import 'package:facerecognitiondtr/services/config_service.dart';
import 'package:facerecognitiondtr/core/api_client.dart';
import 'package:shared_preferences/shared_preferences.dart';

class MockConfigService extends Mock implements ConfigService {}
class MockApiClient extends Mock implements ApiClient {}
class MockDio extends Mock implements Dio {}

void main() {
  late AuthRepository authRepository;
  late MockConfigService mockConfigService;
  late MockApiClient mockApiClient;
  late MockDio mockDio;

  setUp(() {
    SharedPreferences.setMockInitialValues({});
    mockConfigService = MockConfigService();
    mockApiClient = MockApiClient();
    mockDio = MockDio();

    when(() => mockConfigService.getBaseUrl()).thenAnswer((_) async => 'http://test.com');
    when(() => mockApiClient.dio).thenReturn(mockDio);
    when(() => mockApiClient.updateBaseUrl()).thenAnswer((_) async => {});
    when(() => mockDio.options).thenReturn(BaseOptions());
    
    authRepository = AuthRepository(
      configService: mockConfigService,
      apiClient: mockApiClient,
    );
  });

  group('login', () {
    test('throws exception with server error data on 400 error', () async {
      final responseData = {'detail': 'Invalid credentials'};
      final dioException = DioException(
        requestOptions: RequestOptions(path: 'auth/token'),
        response: Response(
          requestOptions: RequestOptions(path: 'auth/token'),
          data: responseData,
          statusCode: 400,
        ),
        type: DioExceptionType.badResponse,
      );

      when(() => mockDio.post(
        any(),
        data: any(named: 'data'),
        options: any(named: 'options'),
      )).thenThrow(dioException);

      expect(
        () => authRepository.login('test@test.com', 'password'),
        throwsA(predicate((e) => 
          e is Exception && 
          e.toString().contains('Invalid credentials')
        )),
      );
    });

    test('throws user friendly exception on connection timeout', () async {
      final dioException = DioException(
        requestOptions: RequestOptions(path: 'auth/token'),
        type: DioExceptionType.connectionTimeout,
        message: 'Connection timed out',
      );

      when(() => mockDio.post(
        any(),
        data: any(named: 'data'),
        options: any(named: 'options'),
      )).thenThrow(dioException);

      expect(
        () => authRepository.login('test@test.com', 'password'),
        throwsA(predicate((e) => 
          e is Exception && 
          (e.toString().contains('Connection timed out') || e.toString().contains('unreachable'))
        )),
      );
    });
  });

  group('register', () {
    test('sends correct data and returns user map on success', () async {
      final mockFile = MockFile();
      when(() => mockFile.readAsBytes()).thenAnswer((_) async => Uint8List.fromList([1, 2, 3]));
      
      final responseData = {
        'id': '550e8400-e29b-41d4-a716-446655440000',
        'email': 'test@test.com',
        'full_name': 'Test User',
      };

      when(() => mockDio.post(
        'auth/register',
        data: any(named: 'data'),
      )).thenAnswer((_) async => Response(
        requestOptions: RequestOptions(path: 'auth/register'),
        data: responseData,
        statusCode: 200,
      ));

      final result = await authRepository.register(
        email: 'test@test.com',
        password: 'password',
        fullName: 'Test User',
        employeeId: 'EMP001',
        imageFile: mockFile,
      );

      expect(result, responseData);
      verify(() => mockDio.post(
        'auth/register',
        data: {
          'email': 'test@test.com',
          'password': 'password',
          'full_name': 'Test User',
          'employee_id': 'EMP001',
          'image_base64': base64Encode([1, 2, 3]),
        },
      )).called(1);
    });
  });
}

class MockFile extends Mock implements File {}

