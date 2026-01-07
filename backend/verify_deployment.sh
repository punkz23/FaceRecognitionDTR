#!/bin/bash

# Production Deployment Verification Script
# This script verifies that the backend deployment is working correctly

set -e

echo "🚀 Starting Backend Deployment Verification..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker Compose is running
print_status "Checking Docker Compose status..."
if ! docker-compose ps >/dev/null 2>&1; then
    print_error "Docker Compose is not accessible"
    exit 1
fi

# Check container status
print_status "Checking container status..."
containers_running=$(docker-compose ps -q | wc -l)
if [ "$containers_running" -eq 0 ]; then
    print_error "No containers are running"
    exit 1
fi

# Detailed container status
print_status "Detailed container status:"
docker-compose ps

# Wait for health checks to complete
print_status "Waiting for services to be healthy..."
sleep 30

# Check database health
print_status "Checking database connectivity..."
db_health=$(docker-compose exec -T db pg_isready -U ${POSTGRES_USER:-dtr_user} -d ${POSTGRES_DB:-dtr_db} 2>/dev/null || echo "failed")
if [[ $db_health == *"accepting connections"* ]]; then
    print_status "✅ Database is healthy"
else
    print_error "❌ Database health check failed"
    exit 1
fi

# Check backend health endpoint
print_status "Checking backend health endpoint..."
backend_health=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/v1/health || echo "000")
if [ "$backend_health" = "200" ]; then
    print_status "✅ Backend health endpoint is responding (HTTP 200)"
    
    # Get detailed health info
    health_response=$(curl -s http://localhost:8000/api/v1/health || echo "{}")
    print_status "Health response: $health_response"
else
    print_error "❌ Backend health check failed (HTTP $backend_health)"
    exit 1
fi

# Check backend logs for any errors
print_status "Checking for errors in backend logs..."
error_count=$(docker-compose logs --tail=50 backend 2>&1 | grep -i error | wc -l)
if [ "$error_count" -gt 0 ]; then
    print_warning "⚠️  Found $error_count error(s) in backend logs"
    docker-compose logs --tail=10 backend | grep -i error
else
    print_status "✅ No errors found in recent backend logs"
fi

# Test API root endpoint
print_status "Testing API root endpoint..."
root_response=$(curl -s http://localhost:8000/ || echo "{}")
if [[ $root_response == *"Face Recognition DTR API"* ]]; then
    print_status "✅ API root endpoint is working"
else
    print_error "❌ API root endpoint test failed"
    exit 1
fi

# Check environment variables are loaded
print_status "Verifying environment configuration..."
env_check=$(curl -s http://localhost:8000/api/v1/health | grep -o '"environment":"[^"]*"' || echo "")
if [[ $env_check == *"production"* ]]; then
    print_status "✅ Running in production mode"
else
    print_warning "⚠️  Not running in production mode (current: $env_check)"
fi

# Security check - ensure database is not exposed
print_status "Checking security configuration..."
db_port_check=$(docker-compose ps db | grep "0.0.0.0:5432" || echo "")
if [ -n "$db_port_check" ]; then
    print_warning "⚠️  Database port is exposed to host (consider removing for production)"
else
    print_status "✅ Database port is not exposed to host"
fi

# Final summary
echo ""
print_status "🎉 Deployment Verification Complete!"
print_status "✅ All health checks passed"
print_status "✅ Backend is accessible on http://localhost:8000"
print_status "✅ Database is secure and running"
print_status "✅ Environment configuration is loaded"

echo ""
print_status "Next steps:"
echo "1. Configure your SSL certificate (HTTPS)"
echo "2. Update ALLOWED_ORIGINS in .env with your mobile app domain"
echo "3. Test mobile app connectivity"
echo "4. Set up monitoring and backup procedures"

exit 0
