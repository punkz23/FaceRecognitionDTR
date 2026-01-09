# Plan: Dynamic Backend URL, Connection Status & Branding

## Phase 1: Branding & Assets [checkpoint: e4d1ffb]
- [x] Task: Update Application Assets (bd1b549)
    - [x] Implement Feature: Copy `doff logo.png` into the project's asset directory and update `pubspec.yaml`.
- [x] Task: Apply Rebranding to Login Screen (9e139a7)
    - [x] Write Tests: Verify the logo and "DOFF TimeSafe" text are present.
    - [x] Implement Feature: Update `LoginScreen` widgets with the new name and logo asset.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Branding & Assets' (Protocol in workflow.md) (e4d1ffb)

## Phase 2: Logic & Connectivity [checkpoint: 07aace5]
- [x] Task: Implement URL Persistence Service (627ac38)
    - [x] Write Tests: Test saving/retrieving URL via mock `SharedPreferences`.
    - [x] Implement Feature: Create `ConfigService` for dynamic URL management.
- [x] Task: Connection Monitoring Logic (2f27d3a)
    - [x] Write Tests: Verify state changes based on health check responses.
    - [x] Implement Feature: Build a `ConnectivityBloc` or similar to poll `/api/v1/health`.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Logic & Connectivity' (Protocol in workflow.md) (07aace5)

## Phase 3: Developer Tools & Final UI [checkpoint: d27fa33]
- [x] Task: Build Hidden Settings Dialog (6fad6a4)
    - [x] Write Tests: Verify 7-tap trigger and URL validation.
    - [x] Implement Feature: Add gesture detector to logo and build the `UrlConfigDialog`.
- [x] Task: Finalize Connection Indicator (1fe2174)
    - [x] Write Tests: Verify button disabling and indicator colors.
    - [x] Implement Feature: Add indicator to Login screen and bind button state.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Developer Tools & Final UI' (Protocol in workflow.md) (d27fa33)
