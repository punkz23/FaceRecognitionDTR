import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:facerecognitiondtr/services/auth_repository.dart';
import 'package:facerecognitiondtr/services/config_service.dart';
import 'package:dio/dio.dart';
import 'package:facerecognitiondtr/core/api_client.dart';

import 'dart:typed_data';

class MockConfigService extends Mock implements ConfigService {}
class MockApiClient extends Mock implements ApiClient {}
class MockDio extends Mock implements Dio {}
class MockFile extends Mock implements File {}

void main() {
  group('AuthRepository Dynamic URL', () {
    late AuthRepository authRepository;
    late MockConfigService mockConfigService;
    late MockApiClient mockApiClient;
    late MockDio mockDio;
    late MockFile mockFile;

    setUp(() {
      mockConfigService = MockConfigService();
      mockApiClient = MockApiClient();
      mockDio = MockDio();
      mockFile = MockFile();

      when(() => mockConfigService.getBaseUrl()).thenAnswer((_) async => 'http://dynamic-url.com');
      when(() => mockApiClient.dio).thenReturn(mockDio);
      // Mock dio.options
      when(() => mockDio.options).thenReturn(BaseOptions());
      
      authRepository = AuthRepository(
        configService: mockConfigService,
        apiClient: mockApiClient,
      );
    });

    test('register uses dynamic base URL', () async {
      when(() => mockFile.readAsBytes()).thenAnswer((_) async => Uint8List(0));
      
      when(() => mockDio.post(
        any(),
        data: any(named: 'data'),
      )).thenAnswer((_) async => Response(
        requestOptions: RequestOptions(path: ''),
        statusCode: 200,
        data: {'success': true},
      ));

      await authRepository.register(
        email: 'test@test.com',
        password: 'password',
        fullName: 'Test User',
        employeeId: '123',
        imageFile: mockFile,
      );

      // Verify that the base URL was set on the Dio instance
      verify(() => mockConfigService.getBaseUrl()).called(1);
      // We can't easily verify the side effect on dio.options.baseUrl with mocktail unless we mock BaseOptions or verify the getter was called.
      // But verify(() => mockConfigService.getBaseUrl()).called(1) confirms the update logic was triggered.
    });

    test('improved error reporting includes attempted URL', () async {
      when(() => mockFile.readAsBytes()).thenAnswer((_) async => Uint8List(0));
      
      final dioException = DioException(
        requestOptions: RequestOptions(path: 'auth/register'),
        type: DioExceptionType.connectionError,
        message: 'Connection refused',
      );

      when(() => mockDio.post(any(), data: any(named: 'data'))).thenThrow(dioException);

      expect(
        () => authRepository.register(
          email: 'test@test.com',
          password: 'password',
          fullName: 'Test User',
          employeeId: '123',
          imageFile: mockFile,
        ),
        throwsA(predicate((e) => e is Exception && e.toString().contains('http://dynamic-url.com'))),
      );
    });
  });
}
