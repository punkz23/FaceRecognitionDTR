# Plan: Approval and Branch Assignment with Location Validation

This plan outlines the steps to implement the enhanced Admin approval workflow, branch management, and strict location validation for attendance.

## Phase 1: Data Model & Schema Updates [checkpoint: 0ec8a8a]
- [x] Task: Update User and Branch Models (0631683)
    - [ ] Write Tests: Create tests to verify the new fields (`User.rejection_reason` and `Branch.address`).
    - [ ] Implement Feature: Update `backend/app/models/models.py` with the new fields.
- [x] Task: Update Pydantic Schemas (897920a)
    - [ ] Write Tests: Create tests for updated Branch and User schemas.
    - [ ] Implement Feature: Update `backend/app/schemas/` for Branch (CRUD) and User (status updates).
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Data Model & Schema Updates' (Protocol in workflow.md)

## Phase 2: Branch Management API [checkpoint: ]
- [ ] Task: Implement Branch CRUD Endpoints
    - [ ] Write Tests: Create integration tests for `POST`, `GET`, `PATCH`, and `DELETE` /branches.
    - [ ] Implement Feature: Create `backend/app/api/v1/endpoints/branches.py` and register it in `api_router.py`.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Branch Management API' (Protocol in workflow.md)

## Phase 3: Enhanced Approval & Rejection Logic [checkpoint: ]
- [ ] Task: Implement Email Service (Mock/Placeholder)
    - [ ] Write Tests: Test a utility that logs email sending.
    - [ ] Implement Feature: Create a simple email service in `backend/app/services/email_service.py`.
- [ ] Task: Update Admin Approval API
    - [ ] Write Tests: Test `PATCH /admin/users/{id}/status` with `branch_id` and verify email "trigger".
    - [ ] Implement Feature: Update `backend/app/api/v1/endpoints/admin.py` to handle branch assignment and email notification on approval.
- [ ] Task: Implement Rejection API
    - [ ] Write Tests: Test `PATCH /admin/users/{id}/status` with `REJECTED` and `rejection_reason`.
    - [ ] Implement Feature: Add rejection logic and email notification with reason.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Enhanced Approval & Rejection Logic' (Protocol in workflow.md)

## Phase 4: Strict Location Validation [checkpoint: ]
- [ ] Task: Implement Distance Calculation Logic
    - [ ] Write Tests: Test Haversine formula (or similar) in a utility function.
    - [ ] Implement Feature: Create `backend/app/core/location_utils.py`.
- [ ] Task: Integrate Location Check in Attendance API
    - [ ] Write Tests: Test `POST /attendance` with coordinates inside and outside the geofence.
    - [ ] Implement Feature: Update `backend/app/api/v1/endpoints/attendance.py` to validate location against the user's assigned branch.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Strict Location Validation' (Protocol in workflow.md)

## Phase 5: Admin Dashboard - Branch UI [checkpoint: ]
- [ ] Task: Build Branch Management Pages
    - [ ] Write Tests: Test rendering of branch list and creation form.
    - [ ] Implement Feature: Create Branch List and Branch Form components/pages in `admin-dashboard`.
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Admin Dashboard - Branch UI' (Protocol in workflow.md)

## Phase 6: Admin Dashboard - Enhanced Approval UI [checkpoint: ]
- [ ] Task: Update Approval Queue UI
    - [ ] Write Tests: Test branch selection in the approval modal and rejection reason input.
    - [ ] Implement Feature: Add face image display, branch selection, and rejection modal to the approval workflow.
- [ ] Task: Conductor - User Manual Verification 'Phase 6: Admin Dashboard - Enhanced Approval UI' (Protocol in workflow.md)

## Phase 7: Mobile App - Status & GPS Handling [checkpoint: ]
- [ ] Task: Implement Rejection Feedback in Login
    - [ ] Write Tests: Mock `REJECTED` status response and verify error message display.
    - [ ] Implement Feature: Update Login flow in Flutter to handle and display `rejection_reason`.
- [ ] Task: Implement GPS Prompt in Attendance
    - [ ] Write Tests: Mock location service disabled and verify prompt.
    - [ ] Implement Feature: Add GPS check and system prompt in the Time In flow.
- [ ] Task: Conductor - User Manual Verification 'Phase 7: Mobile App - Status & GPS Handling' (Protocol in workflow.md)
