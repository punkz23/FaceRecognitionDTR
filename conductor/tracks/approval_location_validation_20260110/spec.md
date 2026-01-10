# Specification: Approval and Branch Assignment with Location Validation

## 1. Overview
This track implements a robust workflow for Administrator approval of new employee registrations, including simultaneous branch assignment. It enforces strict location-based attendance logging, ensuring employees can only clock in when physically present at their assigned branch. Additionally, it provides full Branch Management capabilities for Admins.

## 2. Functional Requirements

### 2.1 Branch Management (Admin Dashboard)
*   **Create/Edit Branch:**
    *   **Fields:**
        *   `Name` (Unique)
        *   `Address` (Text description)
        *   `Latitude` & `Longitude` (Decimal coordinates)
        *   `Radius` (in meters). **Default:** 100 meters (configurable).
    *   **Validation:** Coordinates must be valid. Name must be unique.
*   **List Branches:** View all active branches with their details.

### 2.2 Admin Dashboard - Approval Workflow
*   **Combined Approval & Assignment:** The "Pending Approvals" interface must allow the Admin to select a `Branch` for the user *at the moment of approval*.
*   **Approval Action:**
    *   Admin selects a user from the "Pending" list.
    *   Admin selects a `Branch` from a searchable dropdown.
    *   Admin clicks "Approve".
    *   **System Actions:**
        *   Updates user status to `APPROVED`.
        *   Updates user's `branch_id`.
        *   Sends an automated "Welcome/Approved" email to the user.
*   **Rejection Action:**
    *   Admin clicks "Reject".
    *   Admin *must* provide a `rejection_reason` (text).
    *   **System Actions:**
        *   Updates user status to `REJECTED`.
        *   Stores the `rejection_reason` in the `User` record.
        *   Sends an automated "Registration Rejected" email to the user, including the reason.
*   **User Detail Editing:** Admin must be able to edit the user's Name or Employee ID before finalizing approval.
*   **Identity Verification:** Display the user's face capture image (from registration) alongside their details.

### 2.3 Mobile App - GPS & Login
*   **GPS Enforcement:**
    *   When accessing the "Time In" screen, automatically check if Location Services are enabled.
    *   **Action:** If disabled, prompt the user with a system dialog to enable GPS. Block the attendance flow until location is available.
*   **Rejection Feedback:** If a user with `REJECTED` status attempts to login, display a specific error message including the `rejection_reason`.

### 2.4 Attendance - Location Validation (Strict Enforcement)
*   **Backend Validation:**
    *   The `POST /attendance` endpoint must receive `latitude` and `longitude`.
    *   The backend must retrieve the user's assigned `Branch`.
    *   **Logic:** Calculate the distance between the submitted coordinates and the Branch's coordinates.
    *   **Success:** If distance <= `branch.radius_meters` (Default 100m), process the attendance log.
    *   **Failure:** If distance > `branch.radius_meters` OR no branch is assigned:
        *   Reject the request with a `403 Forbidden` error.
        *   Return a clear error message: "You are outside the allowed area for your assigned branch ([Branch Name])."

## 3. Data Model Changes
*   **User Model:** Add `rejection_reason` (String, nullable).
*   **Branch Model:** Add `address` (String, nullable). Ensure `latitude`, `longitude`, and `radius_meters` are fully implemented and exposed in APIs.

## 4. Non-Functional Requirements
*   **Security:** Location validation logic must reside on the backend.
*   **Accuracy:** Default radius set to 100m to accommodate common GPS drift (5-20m) and building footprints.

## 5. Out of Scope
*   Employee self-selection of branches.
*   Dynamic geofence radius per user (radius is set at the Branch level).
