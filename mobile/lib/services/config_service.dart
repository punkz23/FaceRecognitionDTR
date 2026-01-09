import 'package:shared_preferences/shared_preferences.dart';

class ConfigService {
  static const String _keyBaseUrl = 'api_base_url';
  // Default URL for Android Emulator to localhost
  // Note: For physical devices this should be the computer's IP address
  static const String _defaultBaseUrl = 'http://192.168.1.16:8000';

  Future<String> getBaseUrl() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_keyBaseUrl) ?? _defaultBaseUrl;
  }

  Future<void> saveBaseUrl(String url) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyBaseUrl, url);
  }

  Future<void> resetBaseUrl() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_keyBaseUrl);
  }
}
