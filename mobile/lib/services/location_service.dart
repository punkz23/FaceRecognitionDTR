import 'package:geolocator/geolocator.dart';

class GeolocatorWrapper {
  Future<bool> isLocationServiceEnabled() => Geolocator.isLocationServiceEnabled();
  Future<LocationPermission> checkPermission() => Geolocator.checkPermission();
  Future<LocationPermission> requestPermission() => Geolocator.requestPermission();
  Future<Position> getCurrentPosition() => Geolocator.getCurrentPosition();
}

class LocationService {
  final GeolocatorWrapper _wrapper;

  LocationService({GeolocatorWrapper? wrapper}) : _wrapper = wrapper ?? GeolocatorWrapper();

  Future<Position?> getCurrentLocation() async {
    bool serviceEnabled;
    LocationPermission permission;

    serviceEnabled = await _wrapper.isLocationServiceEnabled();
    if (!serviceEnabled) {
      return null;
    }

    permission = await _wrapper.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await _wrapper.requestPermission();
      if (permission == LocationPermission.denied) {
        return null;
      }
    }
    
    if (permission == LocationPermission.deniedForever) {
      return null;
    } 

    return await _wrapper.getCurrentPosition();
  }
}