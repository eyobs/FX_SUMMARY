#!/bin/bash

# FX Summary Service Startup Script (using uv)

echo "Starting FX Summary Service with uv..."

# Install dependencies using uv
echo "Installing dependencies with uv..."
uv sync

# Start the application
echo "Starting FastAPI application on port 8000..."
echo "API Documentation: http://localhost:8000/docs"
echo "Health check: http://localhost:8000/health"
echo "Summary: http://localhost:8000/summary"
echo ""
echo "Press Ctrl+C to stop the service"

uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
