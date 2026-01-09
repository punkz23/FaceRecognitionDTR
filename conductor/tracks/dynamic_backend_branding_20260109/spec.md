# Specification: Dynamic Backend URL, Connection Status & Branding

## Overview
This track involves two main components:
1.  **Technical Utility:** Allowing dynamic configuration of the backend API URL and providing a real-time connection status indicator on the login screen.
2.  **Branding Update:** Rebranding the application's login interface to "DOFF TimeSafe" and replacing the primary logo.

## User Stories
- **As a Developer/Tester,** I want to switch backend environments without rebuilding the app.
- **As an Employee,** I want to see if the system is online before attempting to log in.
- **As a Stakeholder,** I want the app to reflect our new branding: "DOFF TimeSafe".

## Functional Requirements

### 1. Branding & UI Updates
- **App Name:** Update the main heading/label on the Login screen to **"DOFF TimeSafe"**.
- **Logo Replacement:** Replace the current application logo with the provided asset (`doff logo.png`).
- **Connection Indicator:**
    - A colored circle (Green = Online, Red = Offline) and text label.
    - The "Login" button is disabled if the status is "Offline".

### 2. Hidden Developer Menu
- **Trigger:** Tapping the "DOFF TimeSafe" logo on the Login screen 7 times.
- **Dialog:** A modal allowing users to:
    - View/Edit the API Base URL.
    - Save changes to local storage.

### 3. Backend URL & Persistence
- **Storage:** Persist the custom URL using `shared_preferences`.
- **Connectivity:** Periodically (every 30s) poll the backend health endpoint to update the connection indicator.

## Technical Requirements
- **Assets:** Add `doff logo.png` to the Flutter assets in `pubspec.yaml`.
- **Storage:** `shared_preferences`.
- **Network:** `Dio` for API calls and health checks.

## Acceptance Criteria
- The login page displays "DOFF TimeSafe" and the new logo.
- 7 taps on the logo opens the URL settings.
- The connection indicator accurately shows "Online" or "Offline".
- The Login button is only active when the app is "Online".
