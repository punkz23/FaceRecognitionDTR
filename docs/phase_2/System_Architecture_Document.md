# System Architecture Document (SAD)

## 1. Executive Summary
This document outlines the architectural design for the Face Recognition DTR system. The solution follows a client-server architecture where the Flutter mobile application serves as the client for data capture and user interaction, while a Python-based backend handles business logic, database management, and biometric processing.

## 2. High-Level Architecture
The system consists of three main layers:
1.  **Presentation Layer (Mobile Client):** Flutter application responsible for UI, camera handling, and on-device liveness checks.
2.  **Application Layer (Backend API):** Python FastAPI service managing authentication, attendance rules, and orchestration of the AI engine.
3.  **Data Layer:** PostgreSQL database for relational data and object storage (e.g., AWS S3 or MinIO) for physical image files.

### 2.1 Component Diagram
```
[Flutter App] <--(HTTPS/JSON)--> [API Gateway / Load Balancer]
                                        |
                                        v
                                 [FastAPI Backend]
                                   /           \
                                  /             \
                        [AI Service]       [PostgreSQL DB]
                       (DeepFace/Dlib)      (User/Logs)
```

## 3. Technology Stack

### 3.1 Mobile Client
*   **Framework:** Flutter (Dart)
*   **State Management:** BLoC (Business Logic Component)
*   **Networking:** Dio
*   **ML Integration:** Google ML Kit (Face Detection)

### 3.2 Backend Server
*   **Framework:** FastAPI (Python) - Chosen for high performance and easy integration with ML libraries.
*   **WSGI/ASGI Server:** Uvicorn / Gunicorn
*   **Authentication:** OAuth2 with JWT (JSON Web Tokens)

### 3.3 Artificial Intelligence
*   **Library:** `face_recognition` (dlib-based) or `DeepFace`
*   **Model:** ResNet-34 or FaceNet
*   **Vector Storage:** Raw binary or `pgvector` extension in PostgreSQL

### 3.4 Database & Storage
*   **RDBMS:** PostgreSQL 15+
*   **Object Storage:** Local filesystem (dev) / AWS S3 (prod)

## 4. Security Architecture
*   **Communication:** Enforced HTTPS (TLS 1.2+).
*   **API Security:** Rate limiting, JWT token expiration (15 mins access, 7 days refresh).
*   **Data Protection:** AES-256 encryption for sensitive columns.
