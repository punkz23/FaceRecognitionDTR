# Plan: Approval and Branch Assignment with Location Validation

This plan outlines the steps to implement the enhanced Admin approval workflow, branch management, and strict location validation for attendance.

## Phase 1: Data Model & Schema Updates [checkpoint: 0ec8a8a]
- [x] Task: Update User and Branch Models (0631683)
    - [x] Write Tests: Create tests to verify the new fields (`User.rejection_reason` and `Branch.address`).
    - [x] Implement Feature: Update `backend/app/models/models.py` with the new fields.
- [x] Task: Update Pydantic Schemas (897920a)
    - [x] Write Tests: Create tests for updated Branch and User schemas.
    - [x] Implement Feature: Update `backend/app/schemas/` for Branch (CRUD) and User (status updates).
- [x] Task: Conductor - User Manual Verification 'Phase 1: Data Model & Schema Updates' (Protocol in workflow.md) (0ec8a8a)

## Phase 2: Branch Management API [checkpoint: 7e82033]
- [x] Task: Implement Branch CRUD Endpoints (2adaf4c)
    - [x] Write Tests: Create integration tests for `POST`, `GET`, `PATCH`, and `DELETE` /branches.
    - [x] Implement Feature: Create `backend/app/api/v1/endpoints/branches.py` and register it in `api_router.py`.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Branch Management API' (Protocol in workflow.md) (7e82033)

## Phase 3: Enhanced Approval & Rejection Logic [checkpoint: 016474c]
- [x] Task: Implement Email Service (Mock/Placeholder) (983309e)
    - [x] Write Tests: Test a utility that logs email sending.
    - [x] Implement Feature: Create a simple email service in `backend/app/services/email_service.py`.
- [x] Task: Update Admin Approval API (9536121)
    - [x] Write Tests: Test `PATCH /admin/users/{id}/status` with `branch_id` and verify email "trigger".
    - [x] Implement Feature: Update `backend/app/api/v1/endpoints/admin.py` to handle branch assignment and email notification on approval.
- [x] Task: Implement Rejection API (9536121)
    - [x] Write Tests: Test `PATCH /admin/users/{id}/status` with `REJECTED` and `rejection_reason`.
    - [x] Implement Feature: Add rejection logic and email notification with reason.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Enhanced Approval & Rejection Logic' (Protocol in workflow.md) (016474c)

## Phase 4: Strict Location Validation [checkpoint: 8a58fe6]
- [x] Task: Implement Distance Calculation Logic (4ecced1)
    - [x] Write Tests: Test Haversine formula (or similar) in a utility function.
    - [x] Implement Feature: Create `backend/app/core/location_utils.py`.
- [x] Task: Integrate Location Check in Attendance API (96346f4)
    - [x] Write Tests: Test `POST /attendance` with coordinates inside and outside the geofence.
    - [x] Implement Feature: Update `backend/app/api/v1/endpoints/attendance.py` to validate location against the user's assigned branch.
- [x] Task: Conductor - User Manual Verification 'Phase 4: Strict Location Validation' (Protocol in workflow.md) (8a58fe6)

## Phase 5: Admin Dashboard - Branch UI [checkpoint: 948bb07]
- [x] Task: Build Branch Management Pages (7535fd5)
    - [x] Write Tests: Test rendering of branch list and creation form.
    - [x] Implement Feature: Create Branch List and Branch Form components/pages in `admin-dashboard`.
- [x] Task: Conductor - User Manual Verification 'Phase 5: Admin Dashboard - Branch UI' (Protocol in workflow.md) (948bb07)

## Phase 6: Admin Dashboard - Enhanced Approval UI [checkpoint: e7d320a]
- [x] Task: Update Approval Queue UI (7ec4319)
    - [x] Write Tests: Test branch selection in the approval modal and rejection reason input.
    - [x] Implement Feature: Add face image display, branch selection, and rejection modal to the approval workflow.
- [x] Task: Conductor - User Manual Verification 'Phase 6: Admin Dashboard - Enhanced Approval UI' (Protocol in workflow.md) (e7d320a)

## Phase 7: Mobile App - Status & GPS Handling [checkpoint: 65ec618]
- [x] Task: Implement Rejection Feedback in Login (d8dbcf8)
    - [x] Write Tests: Mock `REJECTED` status response and verify error message display.
    - [x] Implement Feature: Update Login flow in Flutter to handle and display `rejection_reason`.
- [x] Task: Implement GPS Prompt in Attendance (d8dbcf8)
    - [x] Write Tests: Mock location service disabled and verify prompt.
    - [x] Implement Feature: Add GPS check and system prompt in the Time In flow.
- [x] Task: Conductor - User Manual Verification 'Phase 7: Mobile App - Status & GPS Handling' (Protocol in workflow.md) (65ec618)
