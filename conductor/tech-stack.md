# Technology Stack

## Backend
- **Language:** Python
- **Web Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Migration Tool:** Alembic
- **Face Recognition:** `face_recognition` library, OpenCV (`opencv-python-headless`)
- **Containerization:** Docker, Docker Compose
- **Security:** JWT (python-jose), Password hashing (passlib with bcrypt)
- **Configuration:** `pydantic-settings` (for environment variable management)

## Web (Admin Dashboard)
- **Framework:** React (TypeScript)
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **UI Components:** Shadcn/UI (Radix UI + Lucide Icons)

## Mobile
- **Framework:** Flutter (Dart)
- **UI:** Material Design (with Cupertino icons support)
- **Core Libraries:**
    - `dio`: API communication
    - `camera`: Camera interface for face capture
    - `google_mlkit_face_detection`: On-device face detection
    - `geolocator`: GPS location and geofencing
    - `shared_preferences`: Local token storage
    - `flutter_bloc`: State management
    - `equatable`: Value-based object equality

## Development & Deployment
- **Environment Management:** Python venv, `.env` files
- **Testing:** 
    - Backend: `pytest`, `pytest-mock`, `pytest-cov`
    - Web: `vitest`, `@testing-library/react`
    - Mobile: `flutter_test`, `mocktail`