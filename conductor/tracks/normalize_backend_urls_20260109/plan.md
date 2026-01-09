# Plan: Normalize Backend URLs & Fix 404s

## Phase 1: URL Validation & Normalization [checkpoint: 175e99a]
- [x] Task: Implement URL Normalization in ConfigService (4027025)
    - [x] Write Tests: Add unit tests to `config_service_test.dart` for cases like `URL://192...`, `192...`, and `http://192...`.
    - [x] Implement Feature: Update `ConfigService.saveBaseUrl` to normalize input before saving.
- [x] Task: Update Settings Dialog Validation (554c262)
    - [x] Implement Feature: Update `UrlConfigDialog` to show an error if the input looks like the previous malformed `URL://` pattern.
- [x] Task: Conductor - User Manual Verification 'Phase 1: URL Validation' (Protocol in workflow.md) (175e99a)

## Phase 2: Repository & Client Alignment [checkpoint: dd1ef74]
- [x] Task: Audit ApiClient Path Handling (8e944fe)
    - [x] Implement Feature: Update `AuthRepository` and `ApiClient` to use a more robust way of joining paths (e.g., ensuring trailing slashes on base and no leading slashes on segments).
- [x] Task: Conductor - User Manual Verification 'Phase 2: Repository Alignment' (Protocol in workflow.md) (dd1ef74)
