# Plan: Fix Registration Connection Error

## Phase 1: Configuration & Repository Fix
- [x] Task: Update Default Backend IP (f445c54)
    - [x] Implement Feature: Update `ConfigService` default URL to `http://192.168.253.100:8000`.
- [x] Task: Refactor AuthRepository for Dynamic URL (b886aaa)
    - [x] Write Tests: Create unit tests for `AuthRepository.register` verifying it uses the URL from `ConfigService`.
    - [x] Implement Feature: Update `AuthRepository` to fetch the base URL from `ConfigService` before making the registration request.
- [x] Task: Improve Network Error Reporting (21697d2)
    - [x] Write Tests: Verify that connection errors include the attempted URL in the message.
    - [x] Implement Feature: Update the error handling logic in `AuthRepository` to include the base URL in the exception message.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Configuration & Repository Fix' (Protocol in workflow.md)
