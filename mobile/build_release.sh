#!/bin/bash

echo "========================================"
echo "    Face Recognition DTR - Build Tool   "
echo "========================================"

# Check if Flutter is installed
if ! command -v flutter &> /dev/null
then
    echo "Error: Flutter is not installed or not in PATH."
    exit 1
fi

echo "Cleaning project..."
flutter clean
flutter pub get

echo "----------------------------------------"
echo "Select Build Type:"
echo "1) APK (Universal)"
echo "2) App Bundle (AAB - for Play Store)"
echo "----------------------------------------"
read -p "Enter choice [1]: " choice
choice=${choice:-1}

if [ "$choice" -eq 1 ]; then
    echo "Building Release APK..."
    # Note: Ensure key.properties and keystore are set up in android/
    flutter build apk --release
    echo "Build Complete: build/app/outputs/flutter-apk/app-release.apk"
elif [ "$choice" -eq 2 ]; then
    echo "Building App Bundle..."
    flutter build appbundle --release
    echo "Build Complete: build/app/outputs/bundle/release/app-release.aab"
else
    echo "Invalid choice."
    exit 1
fi

echo "========================================"
echo "Done."
