#!/bin/bash

# Franksher FX Summary Service Startup Script

echo "Starting Franksher FX Summary Service..."

# Install dependencies
pip install -r requirements.txt

# Start the application
echo "Starting FastAPI application on port 8000..."
echo "API Documentation: http://localhost:8000/docs"
echo "Health check: http://localhost:8000/api/v1/health"
echo "Summary: http://localhost:8000/api/v1/summary"
echo ""
echo "Press Ctrl+C to stop the service"

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
