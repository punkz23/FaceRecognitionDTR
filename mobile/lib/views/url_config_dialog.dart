import 'package:flutter/material.dart';
import 'package:facerecognitiondtr/services/config_service.dart';

class UrlConfigDialog extends StatefulWidget {
  const UrlConfigDialog({super.key});

  @override
  State<UrlConfigDialog> createState() => _UrlConfigDialogState();
}

class _UrlConfigDialogState extends State<UrlConfigDialog> {
  final _urlController = TextEditingController();
  final _configService = ConfigService();
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadUrl();
  }

  Future<void> _loadUrl() async {
    final url = await _configService.getBaseUrl();
    setState(() {
      _urlController.text = url;
      _isLoading = false;
    });
  }

  Future<void> _saveUrl() async {
    final url = _urlController.text.trim();
    if (url.isEmpty || !url.startsWith('http')) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please enter a valid URL starting with http/https')),
      );
      return;
    }

    await _configService.saveBaseUrl(url);
    if (mounted) {
      Navigator.of(context).pop(true);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Backend URL updated. Please restart app if needed.')),
      );
    }
  }

  Future<void> _resetUrl() async {
    await _configService.resetBaseUrl();
    await _loadUrl();
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Backend Configuration'),
      content: _isLoading
          ? const SizedBox(height: 100, child: Center(child: CircularProgressIndicator()))
          : Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextField(
                  controller: _urlController,
                  decoration: const InputDecoration(
                    labelText: 'API Base URL',
                    hintText: 'http://192.168.1.x:8000',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 8),
                TextButton(
                  onPressed: _resetUrl,
                  child: const Text('Reset to Default'),
                ),
              ],
            ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('Cancel'),
        ),
        ElevatedButton(
          onPressed: _saveUrl,
          child: const Text('Save'),
        ),
      ],
    );
  }
}
