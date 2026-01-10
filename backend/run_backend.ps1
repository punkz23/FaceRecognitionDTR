$env:PYTHONPATH="."
$env:SECRET_KEY="test_secret"
$env:DATABASE_URL="sqlite:///./app.db"
$env:ENVIRONMENT="development"
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
