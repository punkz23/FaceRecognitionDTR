import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:google_mlkit_face_detection/google_mlkit_face_detection.dart';
import 'package:facerecognitiondtr/services/auth_repository.dart';

class FaceEnrollmentScreen extends StatefulWidget {
  final String email;
  final String password;
  final String fullName;
  final String employeeId;

  const FaceEnrollmentScreen({
    super.key,
    required this.email,
    required this.password,
    required this.fullName,
    required this.employeeId,
  });

  @override
  State<FaceEnrollmentScreen> createState() => _FaceEnrollmentScreenState();
}

class _FaceEnrollmentScreenState extends State<FaceEnrollmentScreen> {
  CameraController? _controller;
  bool _isProcessing = false;
  String? _errorMessage;
  FaceDetector? _faceDetector;
  final AuthRepository _authRepository = AuthRepository();

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
      appBar: AppBar(title: const Text('Enroll Face')),
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
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text(
              'Align your face in the oval',
              style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.w500),
            ),
            const SizedBox(height: 16),
            FloatingActionButton.large(
              onPressed: _isProcessing ? null : _handleCapture,
              backgroundColor: Colors.white,
              child: const Icon(Icons.camera, size: 48, color: Color(0xFF0D47A1)),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _handleCapture() async {
    if (_controller == null || !_controller!.value.isInitialized) return;

    setState(() => _isProcessing = true);

    try {
      print('Taking picture...');
      final XFile image = await _controller!.takePicture();
      print('Picture taken: ${image.path}');

      print('Reading picture bytes...');
      final Uint8List imageBytes = await image.readAsBytes();
      print('Bytes read: ${imageBytes.length}');
      
      if (!kIsWeb) {
        print('Processing image for face detection...');
        final inputImage = InputImage.fromBytes(
          bytes: imageBytes,
          metadata: InputImageMetadata(
            size: const Size(720, 1280), // Approximated
            rotation: InputImageRotation.rotation0deg,
            format: InputImageFormat.bgra8888,
            bytesPerRow: 720 * 4,
          ),
        );
        // On mobile, ML Kit still needs a File or specific metadata. 
        // To keep it simple and working on both, we use File only on mobile.
        final faces = await _faceDetector!.processImage(InputImage.fromFilePath(image.path));
        print('Faces detected: ${faces.length}');

        if (faces.isEmpty) {
          print('No face detected.');
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('No face detected. Please try again.')),
            );
          }
          setState(() => _isProcessing = false);
          return;
        }
      }

      print('Calling registration API...');
      // Send to Registration API
      await _authRepository.register(
        email: widget.email,
        password: widget.password,
        fullName: widget.fullName,
        employeeId: widget.employeeId,
        imageBytes: imageBytes,
      );
      print('Registration API call successful.');

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Registration successful! Please wait for admin approval.')),
        );
        // Navigate back to login
        Navigator.of(context).popUntil((route) => route.isFirst);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Registration Error: $e')),
        );
      }
      setState(() => _isProcessing = false);
    }
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
              'Creating Account...',
              style: TextStyle(color: Colors.white, fontSize: 18),
            ),
          ],
        ),
      ),
    );
  }
}
