# User Flow Diagram

## 1. Authentication Flow
```text
[Start]
  |
  v
[Login Screen]
  |--> (Input Email/Password)
  |
  v
[Validate Credentials]
  |--> (Invalid) --> [Show Error "Invalid Login"] --> [Login Screen]
  |
  |--> (Valid) --> [Fetch User Profile] --> [Main Dashboard]
```

## 2. Daily Attendance Flow (Time-In)
```text
[Main Dashboard]
  |
  v
[Tap "Time In" Button]
  |
  v
[Camera Permission Check]
  |--> (Denied) --> [Show Settings Prompt]
  |
  |--> (Allowed) --> [Launch Camera Overlay]
                         |
                         v
                    [Face Detection] <--(Loop)--> [Check Head Position/Lighting]
                         |
                         |--> (Face Detected & Centered)
                         |
                         v
                    [Capture Image]
                         |
                         v
                    [Send to API (POST /clock-in)]
                         |
                         |--> (Processing...)
                         |
                         v
                    [Receive Response]
                         |
                         |--> (Success) --> [Show Green Success Modal] --> [Refresh Dashboard]
                         |
                         |--> (Fail) --> [Show Red Error "Face Not Recognized"] --> [Retry Option]
```

## 3. History Review Flow
```text
[Main Dashboard]
  |
  v
[Tap "History" Tab]
  |
  v
[Select Month/Year]
  |
  v
[List View of Daily Records]
  |
  v
[Tap Record Item] --> [Show Details (Time In/Out, Locations)]
```
