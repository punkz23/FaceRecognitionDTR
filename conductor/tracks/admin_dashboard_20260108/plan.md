# Plan: Admin Dashboard and Employee Registration

This plan outlines the steps to implement the web-based admin dashboard and the mobile employee registration flow.

## Phase 1: Backend User Lifecycle [checkpoint: d85f89a]
- [x] Task: Update User model and schemas for approval status (6b16776)
    - [x] Write Tests: Create tests for the updated User model and status-based logic.
    - [x] Implement Feature: Add `status` field (PENDING, APPROVED, REJECTED) to `User` model and Pydantic schemas.
- [x] Task: Create Public Registration API (c91a8fc)
    - [x] Write Tests: Create integration tests for the public `POST /auth/register` endpoint including face data.
    - [x] Implement Feature: Build the registration endpoint that handles initial face encoding storage in PENDING state.
- [x] Task: Create Admin Approval APIs (a25b7c0)
    - [x] Write Tests: Create tests for `PATCH /admin/users/{user_id}/status` restricted to admins.
    - [x] Implement Feature: Build the status update endpoints for administrators.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Backend User Lifecycle' (Protocol in workflow.md) (d85f89a)

## Phase 2: Mobile Registration Flow [checkpoint: 860a14b]
- [x] Task: Implement Registration Screen in Flutter (acf698c)
    - [x] Write Tests: Create widget tests for the registration form.
    - [x] Implement Feature: Build the UI for Email, Name, Employee ID, and Password.
- [x] Task: Integrate Face Capture into Registration (6b5e338)
    - [x] Write Tests: Create tests for the registration-specific face capture flow.
    - [x] Implement Feature: Re-use `FaceCaptureScreen` logic to capture face data during registration.
- [x] Task: Implement Restricted "Pending" View (20e755d)
    - [x] Write Tests: Test that "Time In" features are disabled for users with PENDING status.
    - [x] Implement Feature: Update `DashboardScreen` to handle the pending account state.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Mobile Registration Flow' (Protocol in workflow.md) (860a14b)

## Phase 3: Admin Dashboard Foundation (React) [checkpoint: 2ba2aff]
- [x] Task: Scaffold React Project (594c6b6)
    - [x] Write Tests: Set up basic testing environment (Vitest/Jest).
    - [x] Implement Feature: Initialize React app with Tailwind CSS and Shadcn/UI in a new `admin-dashboard` directory.
- [x] Task: Implement Admin Authentication (d2faac4)
    - [x] Write Tests: Test login redirection and token storage.
    - [x] Implement Feature: Build the admin login page and secure layout components.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Admin Dashboard Foundation (React)' (Protocol in workflow.md) (2ba2aff)

## Phase 4: Admin Approvals & Management [checkpoint: d84f885]
- [x] Task: Build Registration Approval Queue (18114a8)
    - [x] Write Tests: Test the fetching and rendering of pending users.
    - [x] Implement Feature: Create the UI to view, approve, or reject new registrations.
- [x] Task: Build Employee Management CRUD (59c0249)
    - [x] Write Tests: Test employee editing and face enrollment via web.
    - [x] Implement Feature: Build the tables and forms for full employee record management.
- [x] Task: Conductor - User Manual Verification 'Phase 4: Admin Approvals & Management' (Protocol in workflow.md) (d84f885)

## Phase 5: Attendance & Branch Management
- [x] Task: Build DTR Monitoring Dashboard (35e59d9)
    - [x] Write Tests: Test filtering and status color-coding of logs.
    - [x] Implement Feature: Create the real-time attendance log viewer with location verification status.
- [x] Task: Build Branch Configuration UI (6ceef1c)
    - [x] Write Tests: Test coordinate and radius updates.
    - [x] Implement Feature: Build the branch management interface with map integration.
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Attendance & Branch Management' (Protocol in workflow.md)

## Phase 6: Payroll & Reporting
- [ ] Task: Implement Payroll Calculation Logic
    - [ ] Write Tests: Unit tests for hour calculations and overtime rules.
    - [ ] Implement Feature: Build the backend service or frontend logic for hour summation.
- [ ] Task: Implement Export Functionality (PDF/Excel)
    - [ ] Write Tests: Test the generation of report files.
    - [ ] Implement Feature: Add buttons to download Payslips and Payroll Summaries in PDF and XLSX formats.
- [ ] Task: Conductor - User Manual Verification 'Phase 6: Payroll & Reporting' (Protocol in workflow.md)
