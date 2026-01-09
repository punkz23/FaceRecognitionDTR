# Specification: Fix Registration Connection & Malformed URL

## Overview
This track addresses two critical issues in the Flutter mobile app's network layer:
1.  **Malformed URL Handling:** The app is currently using a `URL://` prefix (likely from a configuration error), causing `_Namespace` errors on web.
2.  **Registration 404:** The registration endpoint is failing with a 404, suggesting the final request path is incorrect when combined with the dynamic base URL.

## Functional Requirements
1.  **URL Normalization in ConfigService:**
    -   Automatically prepend `http://` if the user enters a raw IP/domain without a protocol.
    -   Strip any accidental `URL://` or duplicate protocol prefixes.
    -   Ensure the default URL is `http://192.168.253.100:8000`.
2.  **Robust Path Joining in AuthRepository:**
    -   Verify that the transition from `ConfigService` to `ApiClient` correctly appends `/api/v1/`.
    -   Ensure requests like `auth/register` don't result in malformed paths (e.g., `.../api/v1//auth/register`).
3.  **UI Validation in Settings Dialog:**
    -   Add immediate validation to the Backend Configuration dialog to prevent saving malformed URLs (like those starting with `URL://`).

## Acceptance Criteria
-   Saving `192.168.253.100:8000` in settings automatically converts it to `http://192.168.253.100:8000`.
-   Registration succeeds on both Web and Mobile targeting port 8000.
-   The "404" error is resolved by verifying the endpoint path alignment.
