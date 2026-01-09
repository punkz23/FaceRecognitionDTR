// mobile/lib/core/security_config.dart

// Export the web-safe version by default.
// If the 'dart.library.io' library is available (which it is on mobile/desktop), 
// export the IO-specific version instead.
export 'security_config_web.dart' if (dart.library.io) 'security_config_io.dart';
