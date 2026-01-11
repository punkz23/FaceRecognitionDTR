# FaceRecognitionDTR

This project, FaceRecognitionDTR, is a Daily Time Record system that utilizes face recognition technology. It comprises three main components: a Python backend API, a React-based admin dashboard, and a Flutter mobile application for employee check-ins.

This document outlines the necessary steps and provides automated scripts for setting up the development environment on a new machine.

---

## 1. Project Setup Overview

This project requires setting up a Python backend, a React admin dashboard, and a Flutter mobile application. For convenience, automated setup scripts and a unified launcher are provided.

### 1.1. Prerequisites

Before running the setup scripts, ensure you have the following installed on your system:

*   **Git:** For cloning the repository and managing code.
    *   *Installation:* [https://git-scm.com/downloads](https://git-scm.com/downloads)
*   **Python:** Version 3.9+ required for the backend.
    *   *Installation:* [https://www.python.org/downloads/](https://www.python.org/downloads/)
    *   Ensure `python` or `python3` command is in your PATH.
*   **Node.js:** Version 16+ recommended for the React admin dashboard.
    *   *Installation:* [https://nodejs.org/](https://nodejs.org/)
    *   npm (Node Package Manager) is included with Node.js.
*   **Flutter SDK:** For the mobile application development.
    *   *Installation:* [https://docs.flutter.dev/get-started/install](https://docs.flutter.dev/get-started/install)
    *   Ensure `flutter` command is in your PATH.
*   **Docker (Optional but Recommended):** For containerized setup using Docker Compose.
    *   *Installation:* [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

### 1.2. Project Structure for Setup Scripts

The setup scripts and documentation are organized in the `scripts/` directory at the root of the project:

```
FaceRecognitionDTR/
├── scripts/
│   ├── backend/          # Backend setup scripts
│   ├── frontend/         # Frontend (React) setup scripts
│   ├── mobile/           # Mobile (Flutter) setup scripts
│   ├── start_all.sh      # Unified launcher script (Linux/macOS)
│   ├── start_all.ps1     # Unified launcher script (Windows PowerShell)
│   ├── stop_all.sh       # Unified stopper script (Linux/macOS)
│   └── stop_all.ps1      # Unified stopper script (Windows PowerShell)
└── docs/                 # Troubleshooting guides and notes
    ├── backend_troubleshooting.md
    ├── frontend_troubleshooting.md
    ├── mobile_troubleshooting.md
    └── common_setup_notes.md
```

---

## 2. Automated Setup and Launch

The `start_all` script automates the entire setup process, from prerequisite checks to launching all components.

### 2.1. Running the Unified Launcher

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd FaceRecognitionDTR
    ```
2.  **Make Shell Scripts Executable (Linux/macOS):**
    ```bash
    chmod +x scripts/**/*.sh
    ```
3.  **Execute the Launcher:**
    *   **Linux/macOS:**
        ```bash
        ./scripts/start_all.sh
        ```
    *   **Windows (PowerShell):**
        ```powershell
        .\scripts\start_all.ps1
        ```

4.  **Follow Prompts:**
    *   The script will ask if you want to perform a **full setup** (install dependencies, etc.). Answer `y` or `n`.
    *   It will then ask if you want to **start all components simultaneously**. Answer `y` or `n`.
    *   If Docker Compose is detected and you choose simultaneous startup, it will attempt to use it first.

5.  **Review Output:**
    *   Pay close attention to the console output for any errors or warnings during setup and startup.

### 2.2. Component Setup Details (Automated)

The `start_all` script orchestrates the following actions for each component:

#### 2.2.1. Backend Setup (Python)
*   Checks for Python (3.9+), pip, venv, Git, and Docker.
*   Copies `.env.example` to `.env` and prompts for configuration.
*   Creates and activates a virtual environment (`backend/venv`).
*   Installs dependencies from `requirements.txt` (or `requirements_no_face.txt`).
*   Initializes the database using `backend/init_tables.py`.
*   Starts the backend server (using `run_backend.ps1` or a default Python command).
*   Performs a health check on `http://localhost:8000/health`.

#### 2.2.2. Admin Dashboard Setup (React)
*   Checks for Node.js (16+) and npm.
*   Copies `.env.example` to `.env` in `admin-dashboard/` and prompts for configuration.
*   Navigates to `admin-dashboard/`.
*   Installs npm dependencies (`npm install --legacy-peer-deps`).
*   Starts the development server (`npm run dev`) and attempts to open `http://localhost:3000` in your browser.

#### 2.2.3. Mobile App Setup (Flutter)
*   Checks for Flutter SDK and Android/iOS toolchains.
*   Navigates to `mobile/`.
*   Fetches Flutter dependencies (`flutter pub get`).
*   Lists available devices/emulators and prompts for selection.
*   Launches the app using `flutter run` on the selected device.

---

## 3. Stopping the Application

To stop all running components, use the `stop_all` script.

*   **Linux/macOS:**
    ```bash
    ./scripts/stop_all.sh
    ```
*   **Windows (PowerShell):**
    ```powershell
    .\scripts\stop_all.ps1
    ```
    This script will stop services managed by Docker Compose (if used) and then attempt to stop individual backend and frontend processes.

---

## 4. Docker Compose Alternative

For a more containerized development experience, you can use Docker Compose.

*   **Prerequisite:** Docker Desktop must be installed and running.
*   **Usage:** The `start_all` script will detect `docker-compose.yml` and offer to start services using it if you choose simultaneous startup.
*   **Starting:** Run `./scripts/start_all.sh` (or `.ps1`) and select 'y' for simultaneous start. The script will attempt to run `docker compose up -d`.
*   **Note:** The Flutter mobile app typically needs to be run separately on a device or emulator, even when using Docker Compose.
*   **Stopping:**
    ```bash
    docker compose -f docker-compose.yml down
    ```

---

## 5. Environment Configuration (`.env` Files)

Each component uses a `.env` file for environment-specific settings (database URLs, API keys, secrets, etc.).

*   The setup scripts will create `.env` files from their respective `.env.example` templates if they don't already exist.
*   **It is crucial to review and update these `.env` files with your specific configurations** before running the application. Refer to the `.env.example` files for available variables and their expected formats.

---

## 6. Troubleshooting

If you encounter issues during setup or runtime, please refer to the detailed troubleshooting guides:

*   **Backend:** `docs/backend_troubleshooting.md`
*   **Admin Dashboard (React):** `docs/frontend_troubleshooting.md`
*   **Mobile App (Flutter):** `docs/mobile_troubleshooting.md`
*   **Common Notes:** `docs/common_setup_notes.md`

---