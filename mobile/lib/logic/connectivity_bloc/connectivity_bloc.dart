import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:dio/dio.dart';
import 'package:facerecognitiondtr/services/config_service.dart';
import 'connectivity_event.dart';
import 'connectivity_state.dart';

class ConnectivityBloc extends Bloc<ConnectivityEvent, ConnectivityState> {
  final ConfigService configService;
  final Dio dio;

  ConnectivityBloc({
    required this.configService,
    Dio? dio,
  }) : dio = dio ?? Dio(),
       super(ConnectivityInitial()) {
    on<CheckConnectivity>(_onCheckConnectivity);
  }

  Future<void> _onCheckConnectivity(
    CheckConnectivity event,
    Emitter<ConnectivityState> emit,
  ) async {
    try {
      final baseUrl = await configService.getBaseUrl();
      final response = await dio.get('$baseUrl/api/v1/health');
      
      if (response.statusCode == 200) {
        emit(ConnectivityOnline());
      } else {
        emit(ConnectivityOffline());
      }
    } catch (_) {
      emit(ConnectivityOffline());
    }
  }
}
