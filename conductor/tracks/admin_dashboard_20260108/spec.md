# Specification: Unified Admin Dashboard and Employee Registration

## Overview
This track involves building a comprehensive web-based Administrative Dashboard using React and implementing a self-registration flow within the Flutter mobile app. It introduces an approval workflow where new users register via mobile, and administrators review and approve them before they can perform attendance actions.

## User Stories
- **As a New Employee,** I want to register my account and capture my face using the mobile app so that I can be enrolled in the system without manual HR data entry.
- **As an HR Manager,** I want to review pending registrations on the web dashboard and approve or reject them based on the provided details and face photo.
- **As an Administrator,** I want to monitor real-time DTR logs and manage branch geofencing settings via a modern web interface.
- **As a Payroll Officer,** I want to generate payslips and reports in various formats (PDF, Excel) from verified attendance data.

## Functional Requirements

### 1. Flutter Mobile Registration
- **Registration Form:** Capture Email, Full Name, Employee ID, and Password.
- **Biometric Enrollment:** Integrated camera interface with **Live Face Detection** (ensuring a valid face is present) to capture the initial profile photo.
- **Pending State:** After submission, users can log in but are restricted to a "Pending Approval" view. The "Time In/Out" features remain disabled until approved.

### 2. React Admin Dashboard
- **Approval Queue:** A dedicated section to view, approve, or reject pending mobile registrations.
- **Employee Management:** Full CRUD operations for approved employee profiles.
- **Face Management:** Ability for admins to enroll faces for users who didn't use the mobile registration (Webcam or Upload).
- **Real-time DTR Monitoring:** Dashboard showing live attendance events with location verification markers.
- **Payroll & Reporting:** Work hour calculations and export functionality (PDF, Excel, Print).
- **Branch Management:** Map-based geofence configuration (Coordinates and Radius).
- **RBAC & Settings:** Role management (Super Admin, HR, Branch Manager) and global system configuration.

### 3. Backend (FastAPI) Updates
- **User Model Enhancement:** Add `status` field (e.g., PENDING, APPROVED, REJECTED).
- **Registration API:** Public (or limited) endpoint for new user registration with face data.
- **Approval API:** Admin-only endpoints to change user status.
- **CORS Update:** Ensure secure communication between the React Web app and the FastAPI backend.

## Technical Requirements
- **Web Frontend:** React with Tailwind CSS and Shadcn/UI.
- **Mobile Frontend:** Flutter (Dart).
- **Backend:** FastAPI (Python).
- **Database:** PostgreSQL (SQLAlchemy).

## Acceptance Criteria
- A user can register on the Flutter app, and their account remains in a "Pending" state.
- The "Time In" button is visible but disabled/hidden for pending users in the mobile app.
- Administrators can see the new registration in the Web Dashboard's approval queue.
- Upon approval, the user's mobile app automatically enables attendance features.
- Payroll reports accurately reflect data from approved users only.
