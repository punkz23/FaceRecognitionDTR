# Deployment & Release Guide

## 1. Backend Deployment (Docker)

### Prerequisites
*   Docker & Docker Compose installed on the server.
*   SSL Certificate (e.g., Let's Encrypt) for HTTPS.

### Steps
1.  **Transfer Code:** Copy the `backend/` directory to the server.
2.  **Configure Environment:**
    *   Edit `docker-compose.yml` (or use a `.env` file).
    *   **CRITICAL:** Change `SECRET_KEY` and `POSTGRES_PASSWORD` to strong values.
3.  **Run Containers:**
    ```bash
    cd backend
    docker-compose up -d --build
    ```
4.  **Verify Status:**
    ```bash
    docker-compose ps
    curl http://localhost:8000/api/v1/health
    ```

## 2. Mobile App Release (Android)

### Prerequisites
*   Android Studio / Android SDK installed.
*   Keystore file generated (`keytool -genkey ...`).

### Signing Configuration
1.  Create `android/key.properties`:
    ```properties
    storePassword=YOUR_STORE_PASSWORD
    keyPassword=YOUR_KEY_PASSWORD
    keyAlias=YOUR_KEY_ALIAS
    storeFile=../upload-keystore.jks
    ```
2.  Ensure `android/app/build.gradle` uses this configuration for the `release` build type.

### Building
Run the helper script:
```bash
cd mobile
./build_release.sh
```
*   **APK:** Use for direct installation (sideloading).
*   **AAB:** Use for uploading to Google Play Console.

## 3. Post-Deployment Checklist
*   [ ] Verify mobile app can connect to the remote server URL.
*   [ ] Test Face Enrollment and Verification in the production environment.
*   [ ] Backup the PostgreSQL database volume (`postgres_data`).
