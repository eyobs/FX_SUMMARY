#!/bin/bash

# FX Summary Service - Test Runner with uv

echo "🧪 Running tests with uv..."
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

# Run tests
echo "🔬 Running test suite..."
uv run pytest tests/ -v

echo ""
echo "✅ Tests completed!"
