// mobile/lib/core/security_config.dart
import 'package:flutter/foundation.dart';

export 'security_config_io.dart' if (kIsWeb) 'security_config_web.dart';