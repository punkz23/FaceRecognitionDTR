# Plan: Fix Login 400 Bad Request & Verify Registration

## Phase 1: Diagnosis & Verbose Logging [checkpoint: 0bb8d2c]
- [x] Task: Implement Verbose Error Logging in AuthRepository (7cd4c19)
    - [x] Write Tests: Create a test case in `auth_repository_test.dart` that simulates a 400 error and verifies the exception contains the server's data.
    - [x] Implement Feature: Update the `catch` block in `AuthRepository.login` to print/extract `e.response?.data`.
- [x] Task: Audit Endpoint and Headers (7cd4c19)
    - [x] Implement Feature: Confirm correct endpoint (`auth/token`) and set `Content-Type: application/x-www-form-urlencoded`.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Diagnosis' (Protocol in workflow.md) (b81e775)

## Phase 2: UX Resilience & UI Fixes [checkpoint: 07a3c0d]
- [x] Task: Fix UI Loading State Persistence (329f92c)
    - [x] Write Tests: Add a widget test for `LoginScreen` that triggers a failed login and verifies the `CircularProgressIndicator` is replaced by the login button.
    - [x] Implement Feature: Ensure `AuthBloc` emits a failure state that the UI reacts to by resetting the loading flag.
- [x] Task: Implement Connectivity/Timeout Handling (64ab939)
    - [x] Write Tests: Simulate a network timeout and verify a specific user-friendly message is displayed.
    - [x] Implement Feature: Add `connectTimeout` handling to `ApiClient` or `AuthRepository`.
- [x] Task: Conductor - User Manual Verification 'Phase 2: UX Resilience' (Protocol in workflow.md) (1239cbc)

## Phase 3: Registration Audit & Regression Testing
- [x] Task: Audit Face Registration Flow (61372b6)
    - [x] Implement Feature: Verify the registration request matches the latest backend schema (multi-part vs JSON).
    - [x] Write Tests: Verify `register` method in `AuthRepository` works with mocked success.
- [x] Task: Final End-to-End Verification (61372b6)
    - [x] Implement Feature: Perform manual login and registration walkthrough.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Registration Audit' (Protocol in workflow.md) (61372b6)
