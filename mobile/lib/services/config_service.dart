import 'package:shared_preferences/shared_preferences.dart';

class ConfigService {
  static const String _keyBaseUrl = 'api_base_url';
  // Default URL for Android Emulator to localhost
  // Note: For physical devices this should be the computer's IP address
  static const String _defaultBaseUrl = 'http://192.168.253.100:8000';

  Future<String> getBaseUrl() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_keyBaseUrl) ?? _defaultBaseUrl;
  }

  Future<void> saveBaseUrl(String url) async {
    String normalizedUrl = url.trim();
    
    // Remove "URL://" if present (case insensitive)
    if (normalizedUrl.toUpperCase().startsWith('URL://')) {
      normalizedUrl = normalizedUrl.substring(6).trim();
    }

    // Handle missing protocol
    if (!normalizedUrl.toLowerCase().startsWith('http://') && 
        !normalizedUrl.toLowerCase().startsWith('https://')) {
      normalizedUrl = 'http://$normalizedUrl';
    }

    // Lowercase the protocol
    if (normalizedUrl.toLowerCase().startsWith('http://')) {
      normalizedUrl = 'http://${normalizedUrl.substring(7)}';
    } else if (normalizedUrl.toLowerCase().startsWith('https://')) {
      normalizedUrl = 'https://${normalizedUrl.substring(8)}';
    }

    // Remove trailing slash
    if (normalizedUrl.endsWith('/')) {
      normalizedUrl = normalizedUrl.substring(0, normalizedUrl.length - 1);
    }

    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyBaseUrl, normalizedUrl);
  }

  Future<void> resetBaseUrl() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_keyBaseUrl);
  }
}
