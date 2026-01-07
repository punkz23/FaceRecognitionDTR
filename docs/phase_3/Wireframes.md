# UI Wireframe Specifications

## 1. Login Screen
*   **Header:** App Logo and Title ("SafeTime DTR").
*   **Form:**
    *   `TextField` (Email) - Icon: `email`.
    *   `TextField` (Password) - Icon: `lock`, Obscure text toggle.
*   **Actions:**
    *   `ElevatedButton` ("Login") - Full width.
    *   `TextButton` ("Forgot Password?").

## 2. Main Dashboard (Employee)
*   **AppBar:**
    *   Leading: Profile Avatar.
    *   Title: "Hello, [Name]".
    *   Action: Notification Bell.
*   **Body:**
    *   **Status Card:** Large visual indicator of current status (e.g., "Clocked Out").
    *   **Clock Widget:** Digital clock with current date.
    *   **Action Grid:**
        *   Large Button: "TIME IN" (Green) or "TIME OUT" (Red).
        *   Secondary Button: "Break Start" / "Break End".
    *   **Recent Activity:** Small list showing last 3 logs.
*   **Bottom Navigation Bar:**
    *   Items: Dashboard, History, Profile.

## 3. Face Capture Overlay
*   **Background:** Full-screen camera preview.
*   **Overlay:**
    *   Semi-transparent black layer with a **transparent oval cutout** in the center.
    *   Text Hint: "Position your face within the frame".
*   **Feedback:**
    *   Dynamic Text: "Move Closer", "Hold Still", "Processing...".
    *   Progress Indicator: Circular loader around the capture button (if manual capture is enabled).
*   **Controls:**
    *   Close Button (Top Right).
    *   Flash Toggle (Top Left).

## 4. History Screen
*   **Header:** Month/Year Selector (Dropdown).
*   **Summary Row:** Total Hours, Lates, Absences.
*   **List View:**
    *   **Card Item:**
        *   Left: Date (e.g., "27 Mon").
        *   Center: Time In - Time Out (e.g., "08:00 AM - 05:05 PM").
        *   Right: Status Chip (Green "On Time", Yellow "Late").

## 5. Profile Screen
*   **Header:** Large Profile Photo.
*   **Details:** Name, Employee ID, Department, Email.
*   **Settings:**
    *   "Change Password".
    *   "Enroll Face Model" (Status: Enrolled/Not Enrolled).
    *   "Logout" (Red Text).
