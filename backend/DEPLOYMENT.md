# Production Deployment Instructions

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Copy the environment template
cp .env.example .env

# EDIT THE .env FILE WITH YOUR SECURE VALUES:
# - POSTGRES_PASSWORD: Generate a strong, unique password (for Docker deployment)
# - SECRET_KEY: Generate a 256-bit random key
# - ALLOWED_ORIGINS: Set to your mobile app domain
# - DATABASE_URL: Configure for your database (SQLite for local dev, PostgreSQL for production)
```

### 2. Generate Secure Values
```bash
# Generate strong database password
openssl rand -base64 32

# Generate 256-bit SECRET_KEY
openssl rand -hex 32
```

### 3. Deploy Backend

#### Option A: Docker Deployment (Production)
```bash
# Build and start containers
docker-compose up -d --build

# Verify deployment
chmod +x verify_deployment.sh
./verify_deployment.sh
```

#### Option B: Local Development (Without Docker)
```bash
# Install dependencies
pip install -r requirements.txt

# For face recognition features, install CMake first:
# Windows: Download from cmake.org or use package manager
# macOS: brew install cmake
# Linux: apt install cmake

# Run locally
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Test health endpoint
curl http://localhost:8000/api/v1/health
```

### 4. Manual Verification

#### Docker Deployment
```bash
# Check container status
docker-compose ps

# Test health endpoint
curl http://localhost:8000/api/v1/health

# Check logs
docker-compose logs -f backend
```

#### Local Development
```bash
# Check if server is running
curl http://localhost:8000/api/v1/health

# View application logs (shown in terminal)
# Server runs on http://0.0.0.0:8000
```

## 🔒 Security Features Implemented

- ✅ Environment variables for all secrets
- ✅ Non-root user in production container
- ✅ Database not exposed to host
- ✅ Health checks for all services
- ✅ Resource limits and restart policies
- ✅ Multi-stage Docker build
- ✅ Production CORS configuration

## 📋 Production Checklist

Before going to production, ensure:

- [ ] `.env` file created with strong passwords
- [ ] `SECRET_KEY` is cryptographically secure
- [ ] `ALLOWED_ORIGINS` set to your mobile app domain
- [ ] Database configured (PostgreSQL for production, SQLite for development)
- [ ] SSL certificate configured for HTTPS
- [ ] Database backups configured
- [ ] Monitoring and logging setup
- [ ] Mobile app can connect to production URL
- [ ] Docker Desktop running and network connectivity verified (for Docker deployment)
- [ ] CMake installed if face recognition features are needed

## 🛠️ Troubleshooting

### Docker Deployment Issues

1. **Docker connectivity issues**
   ```bash
   # Check if Docker Desktop is running
   docker info
   
   # Test DNS resolution
   nslookup auth.docker.io 8.8.8.8
   
   # If DNS fails, add to hosts file (admin required):
   # 34.199.138.61 auth.docker.io
   ```

2. **Database connection failed**
   ```bash
   # Check database logs
   docker-compose logs db
   
   # Verify environment variables
   docker-compose config
   ```

3. **Backend not starting**
   ```bash
   # Check backend logs
   docker-compose logs backend
   
   # Rebuild without cache
   docker-compose build --no-cache
   ```

### Local Development Issues

1. **Missing dependencies**
   ```bash
   # Install CMake for face recognition
   # Windows: Download from cmake.org
   # macOS: brew install cmake
   # Linux: apt install cmake
   
   # Then install face recognition
   pip install face_recognition
   ```

2. **Database issues with SQLite**
   ```bash
   # Ensure DATABASE_URL is set to SQLite
   # DATABASE_URL=sqlite:///./dtr_db.sqlite
   
   # Check if database file is created
   ls -la dtr_db.sqlite
   ```

3. **Port already in use**
   ```bash
   # Find process using port 8000
   netstat -ano | findstr :8000
   
   # Kill the process
   taskkill /PID <PID> /F
   ```

### Reset Docker Deployment
```bash
# Stop and remove containers
docker-compose down -v

# Remove images
docker rmi $(docker images "backend_*" -q)

# Redeploy
docker-compose up -d --build
```

### Reset Local Development
```bash
# Remove database file
rm dtr_db.sqlite

# Restart server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📊 Monitoring

### Health Check Endpoint
```json
GET /api/v1/health
{
  "status": "healthy",
  "environment": "production",
  "project": "Face Recognition DTR"
}
```

### Container Monitoring
```bash
# Resource usage
docker stats

# Container health
docker-compose ps
```
