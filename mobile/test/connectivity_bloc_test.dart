import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:facerecognitiondtr/logic/connectivity_bloc/connectivity_bloc.dart';
import 'package:facerecognitiondtr/logic/connectivity_bloc/connectivity_event.dart';
import 'package:facerecognitiondtr/logic/connectivity_bloc/connectivity_state.dart';
import 'package:facerecognitiondtr/services/config_service.dart';
import 'package:dio/dio.dart';

class MockConfigService extends Mock implements ConfigService {}
class MockDio extends Mock implements Dio {}

void main() {
  group('ConnectivityBloc', () {
    late MockConfigService configService;
    late MockDio dio;

    setUp(() {
      configService = MockConfigService();
      dio = MockDio();
      when(() => configService.getBaseUrl()).thenAnswer((_) async => 'http://test.com');
    });

    blocTest<ConnectivityBloc, ConnectivityState>(
      'emits [ConnectivityOnline] when health check succeeds',
      build: () {
        when(() => dio.get(any())).thenAnswer((_) async => Response(
              requestOptions: RequestOptions(path: ''),
              statusCode: 200,
              data: {'status': 'healthy'},
            ));
        return ConnectivityBloc(configService: configService, dio: dio);
      },
      act: (bloc) => bloc.add(CheckConnectivity()),
      expect: () => [isA<ConnectivityOnline>()],
    );

    blocTest<ConnectivityBloc, ConnectivityState>(
      'emits [ConnectivityOffline] when health check fails',
      build: () {
        when(() => dio.get(any())).thenThrow(DioException(
          requestOptions: RequestOptions(path: ''),
        ));
        return ConnectivityBloc(configService: configService, dio: dio);
      },
      act: (bloc) => bloc.add(CheckConnectivity()),
      expect: () => [isA<ConnectivityOffline>()],
    );
  });
}
