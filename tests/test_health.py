"""
Unit tests for health endpoint
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test health endpoint returns correct response"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root_endpoint():
    """Test root endpoint returns API information"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "version" in data
    assert "docs" in data
    assert data["service"] == "FX Summary Microservice"
