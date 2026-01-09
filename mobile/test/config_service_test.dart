import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:facerecognitiondtr/services/config_service.dart';

void main() {
  group('ConfigService', () {
    late ConfigService configService;

    setUp(() {
      SharedPreferences.setMockInitialValues({});
      configService = ConfigService();
    });

    test('getBaseUrl returns default URL when nothing is saved', () async {
      final url = await configService.getBaseUrl();
      expect(url, equals('http://192.168.253.100:8000'));
    });

    test('saveBaseUrl persists the URL', () async {
      await configService.saveBaseUrl('http://10.0.2.2:8000');
      final url = await configService.getBaseUrl();
      expect(url, equals('http://10.0.2.2:8000'));
    });

    test('resetBaseUrl clears the saved URL', () async {
      await configService.saveBaseUrl('http://example.com');
      await configService.resetBaseUrl();
      final url = await configService.getBaseUrl();
      expect(url, equals('http://192.168.253.100:8000'));
    });

    group('URL Normalization', () {
      test('prepends http:// if protocol is missing', () async {
        await configService.saveBaseUrl('192.168.253.100:8000');
        final url = await configService.getBaseUrl();
        expect(url, equals('http://192.168.253.100:8000'));
      });

      test('strips malformed URL:// prefix', () async {
        await configService.saveBaseUrl('URL://192.168.253.100:8000');
        final url = await configService.getBaseUrl();
        expect(url, equals('http://192.168.253.100:8000'));
      });

      test('handles mixed casing and trailing slashes', () async {
        await configService.saveBaseUrl('HTTP://example.com/');
        final url = await configService.getBaseUrl();
        expect(url, equals('http://example.com'));
      });

      test('preserves https://', () async {
        await configService.saveBaseUrl('https://secure.com');
        final url = await configService.getBaseUrl();
        expect(url, equals('https://secure.com'));
      });
    });
  });
}
