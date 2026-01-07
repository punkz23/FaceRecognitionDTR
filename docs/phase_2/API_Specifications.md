# API Specifications (REST)

## 1. General Information
*   **Base URL:** `/api/v1`
*   **Content-Type:** `application/json`
*   **Date Format:** ISO 8601 (`YYYY-MM-DDTHH:mm:ssZ`)

## 2. Authentication
### 2.1 Login
**POST** `/auth/token`
*   **Body:**
    ```json
    {
      "username": "employee@company.com",
      "password": "secret_password"
    }
    ```
*   **Response (200 OK):**
    ```json
    {
      "access_token": "ey...",
      "refresh_token": "ey...",
      "token_type": "bearer",
      "expires_in": 900
    }
    ```

### 2.2 Refresh Token
**POST** `/auth/refresh`
*   **Body:** `{"refresh_token": "..."}`

## 3. Employee Management (Admin Only)
### 3.1 Create Employee
**POST** `/users`
*   **Headers:** `Authorization: Bearer <token>`
*   **Body:**
    ```json
    {
      "employee_id": "EMP-001",
      "full_name": "John Doe",
      "email": "john@company.com",
      "department_id": 1,
      "role": "EMPLOYEE"
    }
    ```

### 3.2 Enroll Face Data
**POST** `/users/{id}/face-enroll`
*   **Description:** Uploads reference images to generate and store face embeddings.
*   **Content-Type:** `multipart/form-data`
*   **Form Data:** `files` (List of image files)
*   **Response (200 OK):**
    ```json
    {
      "message": "Face data enrolled successfully",
      "vectors_generated": 3
    }
    ```

## 4. Attendance Operations
### 4.1 Clock In
**POST** `/attendance/clock-in`
*   **Headers:** `Authorization: Bearer <token>`
*   **Body:**
    ```json
    {
      "image_base64": "/9j/4AAQSkZJRg...",
      "latitude": 14.5995,
      "longitude": 120.9842
    }
    ```
*   **Response (200 OK):**
    ```json
    {
      "status": "success",
      "timestamp": "2023-10-27T08:00:00Z",
      "confidence_score": 0.98
    }
    ```
*   **Response (401 Unauthorized):** Face not recognized.

### 4.2 Clock Out
**POST** `/attendance/clock-out`
*   **Body:** Same as Clock In.

### 4.3 Get History
**GET** `/attendance/history`
*   **Query Params:** `month=10`, `year=2023`
*   **Response (200 OK):**
    ```json
    [
      {
        "date": "2023-10-27",
        "clock_in": "08:00:00",
        "clock_out": "17:00:00",
        "status": "ON_TIME"
      }
    ]
    ```

## 5. System Health
### 5.1 Health Check
**GET** `/health`
*   **Response:** `{"status": "ok", "db": "connected", "ai_engine": "ready"}`
