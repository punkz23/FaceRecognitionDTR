import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:geolocator/geolocator.dart';
import 'package:facerecognitiondtr/services/location_service.dart';

class MockGeolocatorWrapper extends Mock implements GeolocatorWrapper {}     

void main() {
  late LocationService locationService;
  late MockGeolocatorWrapper mockWrapper;

  setUp(() {
    mockWrapper = MockGeolocatorWrapper();
    locationService = LocationService(wrapper: mockWrapper);
  });

  test('getCurrentLocation returns position when service enabled and permission granted', () async {
    final position = Position(
      longitude: 120.0,
      latitude: 14.0,
      timestamp: DateTime.now(),
      accuracy: 1.0,
      altitude: 1.0,
      heading: 1.0,
      speed: 1.0,
      speedAccuracy: 1.0,
      altitudeAccuracy: 1.0,
      headingAccuracy: 1.0,
    );

    when(() => mockWrapper.isLocationServiceEnabled()).thenAnswer((_) async => true);
    when(() => mockWrapper.checkPermission()).thenAnswer((_) async => LocationPermission.whileInUse);
    when(() => mockWrapper.getCurrentPosition()).thenAnswer((_) async => position);

    final result = await locationService.getCurrentLocation();

    expect(result, position);
    verify(() => mockWrapper.getCurrentPosition()).called(1);
  });

  test('getCurrentLocation throws LocationServiceDisabledException when service disabled', () async {   
    when(() => mockWrapper.isLocationServiceEnabled()).thenAnswer((_) async => false);

    expect(() => locationService.getCurrentLocation(), throwsA(isA<LocationServiceDisabledException>()));
    verifyNever(() => mockWrapper.getCurrentPosition());
  });

  test('getCurrentLocation throws exception when permission denied', () async {  
    when(() => mockWrapper.isLocationServiceEnabled()).thenAnswer((_) async => true);
    when(() => mockWrapper.checkPermission()).thenAnswer((_) async => LocationPermission.denied);
    when(() => mockWrapper.requestPermission()).thenAnswer((_) async => LocationPermission.denied);

    expect(() => locationService.getCurrentLocation(), throwsA(isA<Exception>()));
  });
}