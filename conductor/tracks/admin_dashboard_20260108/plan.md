# Plan: Admin Dashboard and Employee Registration

This plan outlines the steps to implement the web-based admin dashboard and the mobile employee registration flow.

## Phase 1: Backend User Lifecycle
- [~] Task: Update User model and schemas for approval status
    - [ ] Write Tests: Create tests for the updated User model and status-based logic.
    - [ ] Implement Feature: Add `status` field (PENDING, APPROVED, REJECTED) to `User` model and Pydantic schemas.
- [ ] Task: Create Public Registration API
    - [ ] Write Tests: Create integration tests for the public `POST /auth/register` endpoint including face data.
    - [ ] Implement Feature: Build the registration endpoint that handles initial face encoding storage in PENDING state.
- [ ] Task: Create Admin Approval APIs
    - [ ] Write Tests: Create tests for `PATCH /admin/users/{user_id}/status` restricted to admins.
    - [ ] Implement Feature: Build the status update endpoints for administrators.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Backend User Lifecycle' (Protocol in workflow.md)

## Phase 2: Mobile Registration Flow
- [ ] Task: Implement Registration Screen in Flutter
    - [ ] Write Tests: Create widget tests for the registration form.
    - [ ] Implement Feature: Build the UI for Email, Name, Employee ID, and Password.
- [ ] Task: Integrate Face Capture into Registration
    - [ ] Write Tests: Create tests for the registration-specific face capture flow.
    - [ ] Implement Feature: Re-use `FaceCaptureScreen` logic to capture face data during registration.
- [ ] Task: Implement Restricted "Pending" View
    - [ ] Write Tests: Test that "Time In" features are disabled for users with PENDING status.
    - [ ] Implement Feature: Update `DashboardScreen` to handle the pending account state.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Mobile Registration Flow' (Protocol in workflow.md)

## Phase 3: Admin Dashboard Foundation (React)
- [ ] Task: Scaffold React Project
    - [ ] Write Tests: Set up basic testing environment (Vitest/Jest).
    - [ ] Implement Feature: Initialize React app with Tailwind CSS and Shadcn/UI in a new `admin-dashboard` directory.
- [ ] Task: Implement Admin Authentication
    - [ ] Write Tests: Test login redirection and token storage.
    - [ ] Implement Feature: Build the admin login page and secure layout components.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Admin Dashboard Foundation (React)' (Protocol in workflow.md)

## Phase 4: Admin Approvals & Management
- [ ] Task: Build Registration Approval Queue
    - [ ] Write Tests: Test the fetching and rendering of pending users.
    - [ ] Implement Feature: Create the UI to view, approve, or reject new registrations.
- [ ] Task: Build Employee Management CRUD
    - [ ] Write Tests: Test employee editing and face enrollment via web.
    - [ ] Implement Feature: Build the tables and forms for full employee record management.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Admin Approvals & Management' (Protocol in workflow.md)

## Phase 5: Attendance & Branch Management
- [ ] Task: Build DTR Monitoring Dashboard
    - [ ] Write Tests: Test filtering and status color-coding of logs.
    - [ ] Implement Feature: Create the real-time attendance log viewer with location verification status.
- [ ] Task: Build Branch Configuration UI
    - [ ] Write Tests: Test coordinate and radius updates.
    - [ ] Implement Feature: Build the branch management interface with map integration.
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Attendance & Branch Management' (Protocol in workflow.md)

## Phase 6: Payroll & Reporting
- [ ] Task: Implement Payroll Calculation Logic
    - [ ] Write Tests: Unit tests for hour calculations and overtime rules.
    - [ ] Implement Feature: Build the backend service or frontend logic for hour summation.
- [ ] Task: Implement Export Functionality (PDF/Excel)
    - [ ] Write Tests: Test the generation of report files.
    - [ ] Implement Feature: Add buttons to download Payslips and Payroll Summaries in PDF and XLSX formats.
- [ ] Task: Conductor - User Manual Verification 'Phase 6: Payroll & Reporting' (Protocol in workflow.md)
