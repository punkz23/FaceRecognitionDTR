// mobile/lib/core/security_config_web.dart
import 'package:dio/dio.dart';

class SecurityConfig {
  static void setupSslPinning(Dio dio) {
    // SSL pinning is not applicable to web platforms.
    // Dio for web uses BrowserHttpClientAdapter which does not support
    // createHttpClient callback for custom certificate verification.
    // The browser handles TLS/SSL itself.
  }
}
