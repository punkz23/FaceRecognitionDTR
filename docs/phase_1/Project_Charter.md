# Project Charter: Face Recognition DTR System

## 1. Project Overview
The Face Recognition-Based Employee Daily Time Record (DTR) system is designed to provide a secure, contactless, and efficient way for employees to log their attendance. By leveraging biometric face recognition, the system eliminates traditional issues like "buddy punching" and physical contact requirements.

## 2. Project Objectives
*   Implement a Flutter-based mobile application for attendance logging.
*   Develop a secure backend for face verification and data management.
*   Ensure high accuracy in identity verification with liveness detection.
*   Provide HR/Admin tools for attendance reporting and user management.

## 3. Stakeholders
*   **Employees:** Primary users of the mobile app for daily logs.
*   **HR/Admin:** Users responsible for managing employees and generating reports.
*   **IT Department:** Responsible for maintaining the infrastructure and security.
*   **Executive Management:** Oversight and project sponsorship.

## 4. High-Level Scope
### In-Scope:
*   Face capture and liveness detection on mobile.
*   Server-side face recognition and embedding matching.
*   REST API for communication.
*   JWT-based authentication and Role-Based Access Control (RBAC).
*   Attendance history and basic reporting.

### Out-of-Scope:
*   Physical hardware installation (kiosks).
*   Full-scale payroll processing (integration only).
*   Legacy fingerprint device integration.

## 5. Success Criteria
*   Face verification accuracy > 98%.
*   System uptime > 99.9%.
*   Positive feedback from 90% of pilot users during UAT.
*   Zero data breaches of biometric information.
