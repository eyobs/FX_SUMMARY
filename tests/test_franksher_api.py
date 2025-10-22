"""
Unit tests for Franksher API service
"""

import pytest
import json
import os
from unittest.mock import patch, AsyncMock, mock_open
from app.services.franksher_api import FranksherAPIService

@pytest.fixture
def api_service():
    """Create API service instance for testing"""
    return FranksherAPIService()

@pytest.fixture
def sample_api_response():
    """Sample API response data"""
    return [
        {"date": "2025-07-01", "rate": 1.087},
        {"date": "2025-07-02", "rate": 1.085},
        {"date": "2025-07-03", "rate": 1.092}
    ]

@pytest.fixture
def sample_local_data():
    """Sample local data file content"""
    return [
        {"date": "2025-07-01", "rate": 1.087, "from": "EUR", "to": "USD"},
        {"date": "2025-07-02", "rate": 1.085, "from": "EUR", "to": "USD"},
        {"date": "2025-07-03", "rate": 1.092, "from": "EUR", "to": "USD"},
        {"date": "2025-07-04", "rate": 1.089, "from": "EUR", "to": "USD"}
    ]

@pytest.mark.asyncio
@patch('httpx.AsyncClient')
async def test_get_fx_data_success(mock_client, api_service, sample_api_response):
    """Test successful API data fetch"""
    # Mock successful HTTP response
    mock_response = AsyncMock()
    mock_response.json.return_value = sample_api_response
    mock_response.raise_for_status.return_value = None
    
    mock_client_instance = AsyncMock()
    mock_client_instance.get.return_value = mock_response
    mock_client.return_value.__aenter__.return_value = mock_client_instance
    
    result = await api_service.get_fx_data("2025-07-01", "2025-07-03")
    
    assert result == sample_api_response
    mock_client_instance.get.assert_called_once()

@pytest.mark.asyncio
@patch('httpx.AsyncClient')
async def test_get_fx_data_api_failure_fallback(mock_client, api_service, sample_local_data):
    """Test API failure with fallback to local data"""
    # Mock API failure
    mock_client_instance = AsyncMock()
    mock_client_instance.get.side_effect = Exception("API Error")
    mock_client.return_value.__aenter__.return_value = mock_client_instance
    
    # Mock local data file
    with patch('builtins.open', mock_open(read_data=json.dumps(sample_local_data))):
        with patch('os.path.exists', return_value=True):
            result = await api_service.get_fx_data("2025-07-01", "2025-07-03")
    
    # Should return filtered local data
    assert len(result) == 3  # Only dates in range
    assert result[0]["date"] == "2025-07-01"
    assert result[0]["rate"] == 1.087

@pytest.mark.asyncio
@patch('httpx.AsyncClient')
async def test_get_fx_data_timeout_retry(mock_client, api_service):
    """Test API timeout with retry logic"""
    # Mock timeout exception
    mock_client_instance = AsyncMock()
    mock_client_instance.get.side_effect = Exception("Timeout")
    mock_client.return_value.__aenter__.return_value = mock_client_instance
    
    # Mock local data fallback
    with patch.object(api_service, '_load_local_data', return_value=[]) as mock_local:
        result = await api_service.get_fx_data("2025-07-01", "2025-07-03")
    
    # Should have tried API multiple times then fallen back
    assert mock_client_instance.get.call_count == api_service.max_retries
    mock_local.assert_called_once()

@pytest.mark.asyncio
async def test_load_local_data_success(api_service, sample_local_data):
    """Test successful local data loading"""
    with patch('builtins.open', mock_open(read_data=json.dumps(sample_local_data))):
        with patch('os.path.exists', return_value=True):
            result = await api_service._load_local_data("2025-07-01", "2025-07-03")
    
    # Should return filtered data
    assert len(result) == 3
    assert all(item["date"] >= "2025-07-01" and item["date"] <= "2025-07-03" for item in result)

@pytest.mark.asyncio
async def test_load_local_data_file_not_found(api_service):
    """Test local data loading when file doesn't exist"""
    with patch('os.path.exists', return_value=False):
        result = await api_service._load_local_data("2025-07-01", "2025-07-03")
    
    assert result == []

@pytest.mark.asyncio
async def test_load_local_data_invalid_json(api_service):
    """Test local data loading with invalid JSON"""
    with patch('builtins.open', mock_open(read_data="invalid json")):
        with patch('os.path.exists', return_value=True):
            result = await api_service._load_local_data("2025-07-01", "2025-07-03")
    
    assert result == []

@pytest.mark.asyncio
@patch('httpx.AsyncClient')
async def test_fetch_from_api_different_response_formats(mock_client, api_service):
    """Test API response with different formats"""
    # Test with rates object format
    rates_response = {
        "rates": {
            "2025-07-01": 1.087,
            "2025-07-02": 1.085,
            "2025-07-03": 1.092
        }
    }
    
    mock_response = AsyncMock()
    mock_response.json.return_value = rates_response
    mock_response.raise_for_status.return_value = None
    
    mock_client_instance = AsyncMock()
    mock_client_instance.get.return_value = mock_response
    mock_client.return_value.__aenter__.return_value = mock_client_instance
    
    result = await api_service._fetch_from_api("2025-07-01", "2025-07-03", "EUR", "USD")
    
    expected = [
        {"date": "2025-07-01", "rate": 1.087},
        {"date": "2025-07-02", "rate": 1.085},
        {"date": "2025-07-03", "rate": 1.092}
    ]
    
    assert result == expected

@pytest.mark.asyncio
@patch('httpx.AsyncClient')
async def test_fetch_from_api_unexpected_format(mock_client, api_service):
    """Test API response with unexpected format"""
    mock_response = AsyncMock()
    mock_response.json.return_value = {"unexpected": "format"}
    mock_response.raise_for_status.return_value = None
    
    mock_client_instance = AsyncMock()
    mock_client_instance.get.return_value = mock_response
    mock_client.return_value.__aenter__.return_value = mock_client_instance
    
    result = await api_service._fetch_from_api("2025-07-01", "2025-07-03", "EUR", "USD")
    
    assert result is None
