# Database Schema Design

## 1. Overview
The database uses **PostgreSQL**. It is normalized to 3NF.

## 2. Entity Relationship Diagram (ERD) Text Representation

*   **Users** (1) ----< (N) **AttendanceLogs**
*   **Users** (1) ----< (N) **FaceEncodings**
*   **Departments** (1) ----< (N) **Users**

## 3. Table Definitions

### 3.1 `departments`
Stores organizational hierarchy.
*   `id` (Serial, PK): Unique identifier.
*   `name` (Varchar, Unique): Department name (e.g., "IT", "HR").
*   `created_at` (Timestamp): Record creation time.

### 3.2 `users`
Stores employee information and login credentials.
*   `id` (UUID, PK): Unique user identifier.
*   `employee_id` (Varchar, Unique): Physical ID card number or company ID.
*   `full_name` (Varchar): Full legal name.
*   `email` (Varchar, Unique): Login email.
*   `password_hash` (Varchar): Bcrypt hash of password.
*   `role` (Enum): 'EMPLOYEE' or 'ADMIN'.
*   `department_id` (Integer, FK): Reference to `departments`.
*   `is_active` (Boolean): Soft delete flag.
*   `created_at` (Timestamp).

### 3.3 `face_encodings`
Stores biometric data. One user can have multiple reference encodings (e.g., with/without glasses).
*   `id` (Serial, PK).
*   `user_id` (UUID, FK): Reference to `users`.
*   `encoding` (ByteA / JSON): The 128-d or 512-d vector array.
*   `version` (Varchar): Model version used (e.g., "dlib_v1").
*   `created_at` (Timestamp).

### 3.4 `attendance_logs`
Stores the daily time records.
*   `id` (UUID, PK).
*   `user_id` (UUID, FK): Reference to `users`.
*   `timestamp` (Timestamp): Exact time of the event.
*   `type` (Enum): 'CLOCK_IN', 'CLOCK_OUT', 'BREAK_START', 'BREAK_END'.
*   `method` (Enum): 'FACE', 'MANUAL_OVERRIDE'.
*   `confidence_score` (Float): The similarity score of the face match (0.0 - 1.0).
*   `snapshot_path` (Varchar): Path to the image captured during the event.
*   `device_info` (Varchar): User agent or device ID.

### 3.5 `audit_logs`
Tracks administrative actions for security.
*   `id` (BigSerial, PK).
*   `actor_id` (UUID, FK): Who performed the action.
*   `action` (Varchar): Description (e.g., "USER_CREATED", "LOG_EDITED").
*   `target_id` (UUID): ID of the affected record.
*   `timestamp` (Timestamp).
