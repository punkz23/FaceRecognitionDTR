# Plan: Dynamic Backend URL, Connection Status & Branding

## Phase 1: Branding & Assets
- [x] Task: Update Application Assets (bd1b549)
    - [x] Implement Feature: Copy `doff logo.png` into the project's asset directory and update `pubspec.yaml`.
- [x] Task: Apply Rebranding to Login Screen (9e139a7)
    - [x] Write Tests: Verify the logo and "DOFF TimeSafe" text are present.
    - [x] Implement Feature: Update `LoginScreen` widgets with the new name and logo asset.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Branding & Assets' (Protocol in workflow.md)

## Phase 2: Logic & Connectivity
- [ ] Task: Implement URL Persistence Service
    - [ ] Write Tests: Test saving/retrieving URL via mock `SharedPreferences`.
    - [ ] Implement Feature: Create `ConfigService` for dynamic URL management.
- [ ] Task: Connection Monitoring Logic
    - [ ] Write Tests: Verify state changes based on health check responses.
    - [ ] Implement Feature: Build a `ConnectivityBloc` or similar to poll `/api/v1/health`.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Logic & Connectivity' (Protocol in workflow.md)

## Phase 3: Developer Tools & Final UI
- [ ] Task: Build Hidden Settings Dialog
    - [ ] Write Tests: Verify 7-tap trigger and URL validation.
    - [ ] Implement Feature: Add gesture detector to logo and build the `UrlConfigDialog`.
- [ ] Task: Finalize Connection Indicator
    - [ ] Write Tests: Verify button disabling and indicator colors.
    - [ ] Implement Feature: Add indicator to Login screen and bind button state.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Developer Tools & Final UI' (Protocol in workflow.md)
