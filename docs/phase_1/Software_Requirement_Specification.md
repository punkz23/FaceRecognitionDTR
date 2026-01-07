# Software Requirement Specification (SRS)

## 1. Introduction
This document details the functional and non-functional requirements for the Face Recognition DTR system.

## 2. Functional Requirements
### 2.1 User Management (Admin)
*   **FR-01:** Admin shall be able to register new employees with a unique ID and full name.
*   **FR-02:** Admin shall be able to enroll employee faces by uploading or capturing multiple reference photos.
*   **FR-03:** Admin shall be able to assign roles (Employee/Admin) and departments.

### 2.2 Attendance Logging (Employee)
*   **FR-04:** The system shall capture a live face image for Time-In/Time-Out actions.
*   **FR-05:** The system shall perform liveness detection to ensure a real person is present.
*   **FR-06:** The system shall match the captured face against the reference embedding in the database.
*   **FR-07:** The system shall record the timestamp and action type (In/Out) upon successful verification.

### 2.3 Business Rules
*   **BR-01:** Employees cannot Clock-In twice without a Clock-Out.
*   **BR-02:** Late arrivals shall be flagged based on a configurable shift start time (e.g., 8:00 AM).
*   **BR-03:** Only one active session is allowed per employee account.

### 2.4 Reporting and History
*   **FR-08:** Employees shall be able to view their own attendance history for the current month.
*   **FR-09:** Admin shall be able to export attendance reports in CSV/PDF format.

## 3. Non-Functional Requirements
### 3.1 Performance
*   **NFR-01:** Face verification response time shall be under 3 seconds.
*   **NFR-02:** The mobile app shall load the dashboard in under 2 seconds on standard hardware.

### 3.2 Security and Privacy
*   **NFR-03:** All biometric data (embeddings) shall be encrypted at rest.
*   **NFR-04:** API communication must use TLS 1.2 or higher.
*   **NFR-05:** Images captured for verification should be stored securely or deleted after processing, depending on policy.

### 3.3 Reliability
*   **NFR-06:** The system shall handle at least 100 concurrent authentication requests during peak hours.

## 4. Hardware Constraints
*   **Camera:** Minimum 5MP front-facing camera required.
*   **Connectivity:** Active internet connection (4G/5G or Wi-Fi) is mandatory for REST API communication.
