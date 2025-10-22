"""
Unit tests for summary endpoint
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)

@pytest.fixture
def sample_fx_data():
    """Sample FX data for testing"""
    return [
        {"date": "2025-07-01", "rate": 1.087, "from": "EUR", "to": "USD"},
        {"date": "2025-07-02", "rate": 1.085, "from": "EUR", "to": "USD"},
        {"date": "2025-07-03", "rate": 1.092, "from": "EUR", "to": "USD"}
    ]

@patch('app.routes.summary.FranksherAPIService')
def test_summary_endpoint_success(mock_api_service, sample_fx_data):
    """Test summary endpoint with successful API response"""
    # Mock the API service
    mock_service_instance = AsyncMock()
    mock_service_instance.get_fx_data.return_value = sample_fx_data
    mock_api_service.return_value = mock_service_instance
    
    response = client.get(
        "/summary?start=2025-07-01&end=2025-07-03"
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check summary format (new simplified format)
    assert "start_rate" in data
    assert "end_rate" in data
    assert "mean_rate" in data
    assert "total_pct_change" in data
    
    assert data["start_rate"] == 1.087
    assert data["end_rate"] == 1.092
    assert data["mean_rate"] == 1.088  # (1.087 + 1.085 + 1.092) / 3

@patch('app.routes.summary.FranksherAPIService')
def test_summary_endpoint_daily_breakdown(mock_api_service, sample_fx_data):
    """Test summary endpoint with daily breakdown"""
    # Mock the API service
    mock_service_instance = AsyncMock()
    mock_service_instance.get_fx_data.return_value = sample_fx_data
    mock_api_service.return_value = mock_service_instance
    
    response = client.get(
        "/summary?start=2025-07-01&end=2025-07-03&breakpoint=day"
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check daily breakdown format (now returns array directly)
    assert isinstance(data, list)
    assert len(data) == 3
    
    # Check first day (no percent change)
    assert data[0]["date"] == "2025-07-01"
    assert data[0]["rate"] == 1.087
    assert data[0]["pct_change"] is None
    
    # Check second day
    assert data[1]["date"] == "2025-07-02"
    assert data[1]["rate"] == 1.085
    assert data[1]["pct_change"] == -0.18  # (1.085 - 1.087) / 1.087 * 100

def test_summary_endpoint_missing_parameters():
    """Test summary endpoint with missing required parameters"""
    response = client.get("/summary")
    assert response.status_code == 422  # Validation error

def test_summary_endpoint_invalid_date_format():
    """Test summary endpoint with invalid date format"""
    response = client.get(
        "/summary?start=invalid-date&end=2025-07-03"
    )
    assert response.status_code == 400
    assert "Invalid date format" in response.json()["detail"]

def test_summary_endpoint_invalid_breakpoint():
    """Test summary endpoint with invalid breakpoint parameter"""
    response = client.get(
        "/summary?start=2025-07-01&end=2025-07-03&breakpoint=invalid"
    )
    assert response.status_code == 400
    assert "Invalid breakpoint parameter" in response.json()["detail"]

def test_summary_endpoint_start_after_end():
    """Test summary endpoint with start date after end date"""
    response = client.get(
        "/summary?start=2025-07-03&end=2025-07-01"
    )
    assert response.status_code == 400
    assert "Start date must be before or equal to end date" in response.json()["detail"]

@patch('app.routes.summary.FranksherAPIService')
def test_summary_endpoint_no_data(mock_api_service):
    """Test summary endpoint when no data is available"""
    # Mock the API service to return empty data
    mock_service_instance = AsyncMock()
    mock_service_instance.get_fx_data.return_value = []
    mock_api_service.return_value = mock_service_instance
    
    response = client.get(
        "/summary?start=2025-07-01&end=2025-07-03"
    )
    
    assert response.status_code == 404
    assert "No FX data available" in response.json()["detail"]
