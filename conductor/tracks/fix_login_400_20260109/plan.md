# Plan: Fix Login 400 Bad Request & Verify Registration

## Phase 1: Diagnosis & Verbose Logging
- [x] Task: Implement Verbose Error Logging in AuthRepository (7cd4c19)
    - [x] Write Tests: Create a test case in `auth_repository_test.dart` that simulates a 400 error and verifies the exception contains the server's data.
    - [x] Implement Feature: Update the `catch` block in `AuthRepository.login` to print/extract `e.response?.data`.
- [x] Task: Audit Endpoint and Headers (7cd4c19)
    - [x] Implement Feature: Confirm correct endpoint (`auth/token`) and set `Content-Type: application/x-www-form-urlencoded`.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Diagnosis' (Protocol in workflow.md)

## Phase 2: UX Resilience & UI Fixes
- [ ] Task: Fix UI Loading State Persistence
    - [ ] Write Tests: Add a widget test for `LoginScreen` that triggers a failed login and verifies the `CircularProgressIndicator` is replaced by the login button.
    - [ ] Implement Feature: Ensure `AuthBloc` emits a failure state that the UI reacts to by resetting the loading flag.
- [ ] Task: Implement Connectivity/Timeout Handling
    - [ ] Write Tests: Simulate a network timeout and verify a specific user-friendly message is displayed.
    - [ ] Implement Feature: Add `connectTimeout` handling to `ApiClient` or `AuthRepository`.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: UX Resilience' (Protocol in workflow.md)

## Phase 3: Registration Audit & Regression Testing
- [ ] Task: Audit Face Registration Flow
    - [ ] Implement Feature: Verify the registration request matches the latest backend schema (multi-part vs JSON).
    - [ ] Write Tests: Verify `register` method in `AuthRepository` works with mocked success.
- [ ] Task: Final End-to-End Verification
    - [ ] Implement Feature: Perform manual login and registration walkthrough.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Registration Audit' (Protocol in workflow.md)
