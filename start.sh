#!/bin/bash

# FX Summary Service - Quick Start with uv

echo "🚀 Starting FX Summary Service with uv..."
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
uv sync

# Start the service
echo "🌐 Starting FastAPI service on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "❤️  Health Check: http://localhost:8000/health"
echo "📊 Summary Endpoint: http://localhost:8000/summary"
echo ""
echo "Press Ctrl+C to stop the service"
echo ""

uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
