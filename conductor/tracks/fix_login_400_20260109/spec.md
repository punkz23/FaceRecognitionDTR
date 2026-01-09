# Specification: Fix Login 400 Bad Request & Verify Registration

## Overview
This track addresses a critical "400 Bad Request" error during the login flow in the mobile application. The goal is to identify the root cause by implementing detailed error logging, ensuring request compatibility with the FastAPI backend, and improving the overall resilience and UX of the authentication system. Additionally, the face registration flow will be audited to ensure it remains functional.

## Functional Requirements
1.  **Detailed Error Logging:**
    -   Modify `AuthRepository` to capture and print the specific server error message contained in `e.response?.data` when a `DioException` occurs.
2.  **Request Audit & Fix:**
    -   Verify the login endpoint path (e.g., `auth/token` vs `auth/login`).
    -   Ensure the `Content-Type` header matches the server's expectation (e.g., `application/x-www-form-urlencoded` for standard FastAPI OAuth2).
    -   Validate that both `email` (as `username`) and `password` are being sent correctly.
3.  **Connectivity Resilience:**
    -   Implement handling for connection timeouts or unreachable server scenarios (e.g., when `192.168.253.100` is offline).
4.  **UI State Management:**
    -   Ensure the loading indicator in the `LoginScreen` is properly dismissed when a 400 error (or any network error) occurs.
5.  **Registration Flow Audit:**
    -   Perform a full walkthrough of the face registration process to ensure the 400 error fix hasn't introduced regressions or to identify if it shares the same root cause.

## Acceptance Criteria
-   The user can successfully log in using valid credentials.
-   On failure, the debug console displays a clear technical reason from the server (e.g., "Invalid username or password").
-   The app provides a user-friendly message (SnackBar/Dialog) for network errors instead of getting stuck on a loading screen.
-   Face registration completes successfully with an approved status in the backend.
