# Specification: Unified Mobile Check-in for Branches

## Overview
This track focuses on replacing the manual "selfie + messenger" attendance process at branches with a streamlined, automated mobile check-in feature. The mobile app will capture the employee's face and GPS coordinates, validate them against the branch's location, and sync the data to the central FastAPI server.

## User Stories
- **As an employee at a branch,** I want to clock in quickly using my phone so that I don't have to send manual photos to a messenger group.
- **As an HR manager,** I want to be certain that the person clocking in is actually who they say they are and is physically present at the branch.

## Technical Requirements
- **Mobile (Flutter):**
    - Face capture UI using the camera.
    - GPS location retrieval and validation.
    - API integration with the FastAPI backend.
- **Backend (FastAPI):**
    - Endpoint for receiving attendance records (photo + coordinates).
    - Integration with `face_recognition` for biometric verification.
    - PostgreSQL storage for attendance logs.

## Success Criteria
- Employees can successfully clock in via the mobile app.
- Attendance records correctly store face verification results and location data.
- The manual messenger group workflow is no longer required for branches using the app.
