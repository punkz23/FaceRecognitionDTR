import 'dart:io';
import 'package:dio/dio.dart';
import 'package:dio/io.dart';

class SecurityConfig {
  // SHA-256 fingerprint of the server's certificate (Placeholder)
  // static const String _fingerprint = "AA:BB:CC:DD:EE:FF:00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF:00:11:22:33:44:55:66:77:88:99";

  static void setupSslPinning(Dio dio) {
    (dio.httpClientAdapter as IOHttpClientAdapter).createHttpClient = () {
      final client = HttpClient();
      client.badCertificateCallback = (X509Certificate cert, String host, int port) {
        // Implement certificate pinning logic here
        // For development (self-signed certs), we might return true temporarily
        // BUT in production, we must verify the fingerprint
        
        // return cert.sha256.toString().toUpperCase() == _fingerprint;
        return true; // DANGEROUS: Only for dev with self-signed certs
      };
      return client;
    };
  }
}
