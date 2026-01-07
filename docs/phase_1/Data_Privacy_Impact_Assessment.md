# Data Privacy Impact Assessment (DPIA)

## 1. Data Collection
The system collects the following Personal Identifiable Information (PII):
*   Full Name
*   Employee ID
*   Biometric Face Images (during enrollment)
*   Biometric Face Embeddings (mathematical representations)
*   Attendance Timestamps
*   Geolocation (optional, for geofencing)

## 2. Purpose of Data Processing
*   Identity verification for attendance logging.
*   Preventing unauthorized "buddy punching".
*   Payroll accuracy and audit trails.

## 3. Data Storage and Security
*   **Embeddings:** Raw images are converted to numerical vectors (embeddings). Only embeddings are used for matching.
*   **Encryption:** Data at rest is encrypted using AES-256. Data in transit is secured via HTTPS/TLS.
*   **Retention:** Biometric data is purged within 30 days of employee termination.

## 4. Risks and Mitigations
| Risk | Severity | Mitigation Strategy |
| :--- | :--- | :--- |
| Unauthorized access to embeddings | High | Implement RBAC and DB-level encryption. |
| Identity spoofing (photos/videos) | Medium | Implement active/passive liveness detection. |
| Data leakage during transit | Medium | Enforce strict TLS certificate pinning. |

## 5. Compliance
The system follows the principle of **Data Minimization**—only capturing the minimum biometric data required for verification. Users must provide explicit consent during the enrollment process.
