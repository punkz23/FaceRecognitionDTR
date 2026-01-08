# Plan: Unified Mobile Check-in for Branches

This plan outlines the steps to implement the automated mobile check-in system.

## Phase 1: Backend Foundation
- [x] Task: Define Attendance database model and schema (97d8d55)
    - [x] Write Tests: Create tests for the Attendance SQLAlchemy model and Pydantic schemas.
    - [x] Implement Feature: Update `backend/app/models/models.py` and create schemas.
- [~] Task: Create Attendance API endpoint
    - [~] Write Tests: Create integration tests for the `POST /attendance` endpoint.
    - [ ] Implement Feature: Build the FastAPI router and controller for attendance submission.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Backend Foundation' (Protocol in workflow.md)

## Phase 2: Face Verification Integration
- [ ] Task: Implement Face Matching logic in `face_service.py`
    - [ ] Write Tests: Create unit tests for face encoding and comparison.
    - [ ] Implement Feature: Enhance `face_service.py` to handle verification against stored employee profiles.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Face Verification Integration' (Protocol in workflow.md)

## Phase 3: Mobile App Core Flow
- [ ] Task: Implement Face Capture UI in Flutter
    - [ ] Write Tests: Create widget tests for the face capture screen.
    - [ ] Implement Feature: Build the camera interface in the mobile app.
- [ ] Task: Implement Location Validation in Flutter
    - [ ] Write Tests: Create unit tests for location service integration.
    - [ ] Implement Feature: Add GPS coordinate retrieval to the check-in flow.
- [ ] Task: Integrate Mobile Check-in with Backend API
    - [ ] Write Tests: Create integration tests for the mobile-to-backend communication.
    - [ ] Implement Feature: Connect the UI, location, and camera to the attendance API.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Mobile App Core Flow' (Protocol in workflow.md)
