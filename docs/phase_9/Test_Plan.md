# Test Plan & Quality Assurance Strategy

## 1. Unit & Integration Testing
*   **Backend:**
    *   Run `pytest` to verify API endpoints (Auth, Users, Attendance).
    *   Verify JWT token generation and validation.
    *   Test Database CRUD operations.
*   **Mobile:**
    *   Run `flutter test` to verify UI rendering (Login, Dashboard).
    *   Test State Management logic (AuthBloc).

## 2. Biometric Accuracy Testing
**Objective:** Measure False Acceptance Rate (FAR) and False Rejection Rate (FRR).
**Procedure:**
1.  **Enrollment:** Enroll 10 test subjects with 3 photos each (Front, Left, Right).
2.  **Positive Match Test:** Each subject attempts to Clock In 10 times in different lighting.
3.  **Negative Match Test:** 5 non-enrolled subjects attempt to Clock In.
4.  **Spoof Attack Test:** Attempt to Clock In using a high-res photo of an enrolled subject on a phone screen.

**Success Metrics:**
*   **FRR (False Rejection):** < 5% (Valid users denied).
*   **FAR (False Acceptance):** < 0.1% (Impostors accepted).
*   **Spoof Detection:** 100% rejection of static photo attacks.

## 3. Load & Performance Testing
**Objective:** Ensure system stability under peak load (e.g., 8:00 AM shift start).
**Procedure:**
1.  Use `load_test.py` script.
2.  Simulate 50-100 concurrent requests within 1 minute.
3.  Monitor Server CPU/Memory usage.
4.  Measure API response time (Target: < 2 seconds).

## 4. User Acceptance Testing (UAT)
**Objective:** Validate usability with real users.
**Scenarios:**
*   **Scenario A:** Employee Enrolls Face -> Logs In -> Clocks In -> Clocks Out.
*   **Scenario B:** Admin creates new department -> Assigns user -> Generates Report.
*   **Scenario C:** User tries to clock in with no internet connection (Verify Error Message).

## 5. Security Audit
*   Verify SSL Pinning is active (Monitor network traffic with proxy).
*   Check Database for unencrypted passwords or embeddings.
*   Attempt API access without a Bearer Token (Expect 401).
