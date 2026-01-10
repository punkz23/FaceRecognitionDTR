import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:google_mlkit_face_detection/google_mlkit_face_detection.dart';
import 'package:facerecognitiondtr/services/attendance_repository.dart';
import 'package:facerecognitiondtr/services/location_service.dart';
import 'package:geolocator/geolocator.dart';
import 'package:dio/dio.dart';

class FaceCaptureScreen extends StatefulWidget {
  const FaceCaptureScreen({super.key});

  @override
  State<FaceCaptureScreen> createState() => _FaceCaptureScreenState();
}

class _FaceCaptureScreenState extends State<FaceCaptureScreen> {
  CameraController? _controller;
  bool _isProcessing = false;
  String? _errorMessage;
  FaceDetector? _faceDetector;
  final AttendanceRepository _attendanceRepository = AttendanceRepository();
  final LocationService _locationService = LocationService();

  @override
  void initState() {
    super.initState();
    if (!kIsWeb) {
      _faceDetector = FaceDetector(
        options: FaceDetectorOptions(
          enableContours: true,
          enableClassification: true,
        ),
      );
    }
    _initializeCamera();
    _checkLocationStatus();
  }

  Future<void> _checkLocationStatus() async {
    try {
      final enabled = await Geolocator.isLocationServiceEnabled();
      if (!enabled && mounted) {
        _showGpsDialog();
      }
    } catch (e) {
      debugPrint('Error checking location status: $e');
    }
  }

  void _showGpsDialog() {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        title: const Text('GPS Disabled'),
        content: const Text('Please enable location services (GPS) to record your attendance.'),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              Geolocator.openLocationSettings();
            },
            child: const Text('Open Settings'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              Navigator.pop(context);
            },
            child: const Text('Cancel'),
          ),
        ],
      ),
    );
  }

  Future<void> _initializeCamera() async {
    try {
      final cameras = await availableCameras();
      if (cameras.isEmpty) {
        setState(() => _errorMessage = 'No cameras found');
        return;
      }

      CameraDescription? selectedCamera;
      try {
        selectedCamera = cameras.firstWhere(
          (camera) => camera.lensDirection == CameraLensDirection.front,
        );
      } catch (_) {
        selectedCamera = cameras.first;
      }

      _controller = CameraController(
        selectedCamera,
        ResolutionPreset.medium,
        enableAudio: false,
      );

      await _controller!.initialize();
      if (mounted) setState(() {});
    } catch (e) {
      setState(() => _errorMessage = 'Camera error: $e');
    }
  }

  @override
  void dispose() {
    _controller?.dispose();
    _faceDetector?.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_errorMessage != null) {
      return Scaffold(
        appBar: AppBar(),
        body: Center(child: Text(_errorMessage!, style: const TextStyle(color: Colors.red))),
      );
    }

    if (_controller == null || !_controller!.value.isInitialized) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    return Scaffold(
      body: Stack(
        fit: StackFit.expand,
        children: [
          CameraPreview(_controller!),
          _buildOverlay(),
          _buildCaptureButton(),
          if (_isProcessing) _buildLoadingOverlay(),
        ],
      ),
    );
  }

  Widget _buildOverlay() {
    return ColorFiltered(
      colorFilter: ColorFilter.mode(
        Colors.black.withValues(alpha: 0.7),
        BlendMode.srcOut,
      ),
      child: Stack(
        children: [
          Container(
            decoration: const BoxDecoration(
              color: Colors.black,
              backgroundBlendMode: BlendMode.dstOut,
            ),
          ),
          Align(
            alignment: Alignment.center,
            child: Container(
              height: 350,
              width: 250,
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(150),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCaptureButton() {
    return Positioned(
      bottom: 48,
      left: 0,
      right: 0,
      child: Center(
        child: FloatingActionButton.large(
          onPressed: _isProcessing ? null : () async {
            if (_controller == null || !_controller!.value.isInitialized) return;

            setState(() => _isProcessing = true);

            try {
              final position = await _locationService.getCurrentLocation();
              final XFile image = await _controller!.takePicture();
              final Uint8List imageBytes = await image.readAsBytes();
              
              if (!kIsWeb) {
                final faces = await _faceDetector!.processImage(InputImage.fromFilePath(image.path));

                if (faces.isEmpty) {
                  if (mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('No face detected. Please try again.')),
                    );
                  }
                  setState(() => _isProcessing = false);
                  return;
                }
              }

              // Send to API
              final result = await _attendanceRepository.clockIn(
                imageBytes,
                position?.latitude,
                position?.longitude,
              );

              if (mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Success: ${result['message'] ?? 'Clocked in successfully'}')),
                );
                Navigator.of(context).pop();
              }
            } on LocationServiceDisabledException {
              if (mounted) {
                _showGpsDialog();
              }
              setState(() => _isProcessing = false);
            } on DioException catch (e) {
              String errorMsg = 'Failed to record attendance.';
              if (e.response?.statusCode == 403) {
                final detail = e.response?.data?['detail'];
                errorMsg = detail ?? 'You are not authorized or outside the allowed branch area.';
              } else if (e.response?.data != null) {
                errorMsg = e.response?.data['detail'] ?? e.message;
              }
              if (mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text(errorMsg), backgroundColor: Colors.red),
                );
              }
              setState(() => _isProcessing = false);
            } catch (e) {
              if (mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Error: $e')),
                );
              }
              setState(() => _isProcessing = false);
            }
          },
          backgroundColor: Colors.white,
          child: const Icon(Icons.camera, size: 48, color: Color(0xFF0D47A1)),
        ),
      ),
    );
  }

  Widget _buildLoadingOverlay() {
    return Container(
      color: Colors.black54,
      child: const Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            CircularProgressIndicator(color: Colors.white),
            SizedBox(height: 16),
            Text(
              'Verifying Identity...',
              style: TextStyle(color: Colors.white, fontSize: 18),
            ),
          ],
        ),
      ),
    );
  }
}
