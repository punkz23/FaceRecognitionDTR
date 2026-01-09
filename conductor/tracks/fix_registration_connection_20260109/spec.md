# Specification: Fix Registration Connection Error

## Overview
The mobile app currently fails during the registration flow, specifically after face capture, with a `Connection refused` error pointing to `localhost`. This indicates that the network layer is attempting to reach the backend at an incorrect address, ignoring the intended IP configuration.

## Problem Description
- **Symptom:** "Registration Error: Exception: Registration failed: DioException [connection error]: ... address = localhost, port = 56848"
- **Trigger:** Pressing the "Capture" button during face registration.
- **Root Cause:** Hardcoded `localhost` reference or lack of integration with `ConfigService` in the registration data submission path.

## Functional Requirements

### 1. Update Default Backend URL
- Change the hardcoded default URL in `ConfigService` from `192.168.1.16` to `192.168.253.100`.

### 2. Ensure Dynamic URL Usage in AuthRepository
- Audit `AuthRepository` and ensure all methods (Login, Register, etc.) retrieve the base URL from `ConfigService` instead of using a hardcoded string or default `Dio` configuration.

### 3. Error Handling Improvement
- Ensure that if a connection error occurs, the error message displayed to the user includes the actual URL being attempted (to aid in future troubleshooting).

## Technical Requirements
- **Service:** `ConfigService` update.
- **Repository:** `AuthRepository` refactor.
- **Network:** `Dio` client configuration.

## Acceptance Criteria
- The "address = localhost" error no longer appears in logs when the backend is unreachable at the correct IP.
- Registration data is successfully sent to `192.168.253.100`.
- Unit tests for `AuthRepository` verify that the dynamic URL from `ConfigService` is used for the registration endpoint.
