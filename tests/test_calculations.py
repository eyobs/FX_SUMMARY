"""
Unit tests for FX calculations
"""

import pytest
from app.services.calculations import FXCalculator

def test_calculate_daily_percent_change():
    """Test daily percent change calculation"""
    rates = [1.087, 1.085, 1.092]
    changes = FXCalculator.calculate_daily_percent_change(rates)
    
    assert changes[0] is None  # First day has no previous rate
    assert changes[1] == -0.18  # (1.085 - 1.087) / 1.087 * 100
    assert changes[2] == 0.65   # (1.092 - 1.085) / 1.085 * 100

def test_calculate_daily_percent_change_with_zero():
    """Test daily percent change calculation with zero rate"""
    rates = [1.087, 0, 1.092]
    changes = FXCalculator.calculate_daily_percent_change(rates)
    
    assert changes[0] is None
    assert changes[1] == -100.0  # (0 - 1.087) / 1.087 * 100
    assert changes[2] is None  # Previous rate is 0

def test_calculate_daily_percent_change_empty():
    """Test daily percent change calculation with empty list"""
    rates = []
    changes = FXCalculator.calculate_daily_percent_change(rates)
    assert changes == []

def test_calculate_daily_percent_change_single():
    """Test daily percent change calculation with single rate"""
    rates = [1.087]
    changes = FXCalculator.calculate_daily_percent_change(rates)
    assert changes == [None]

def test_calculate_mean_rate():
    """Test mean rate calculation"""
    rates = [1.087, 1.085, 1.092]
    mean = FXCalculator.calculate_mean_rate(rates)
    expected = (1.087 + 1.085 + 1.092) / 3
    assert mean == round(expected, 6)

def test_calculate_mean_rate_empty():
    """Test mean rate calculation with empty list"""
    rates = []
    mean = FXCalculator.calculate_mean_rate(rates)
    assert mean == 0.0

def test_calculate_total_percent_change():
    """Test total percent change calculation"""
    start_rate = 1.087
    end_rate = 1.092
    total_change = FXCalculator.calculate_total_percent_change(start_rate, end_rate)
    expected = ((1.092 - 1.087) / 1.087) * 100
    assert total_change == round(expected, 2)

def test_calculate_total_percent_change_zero_start():
    """Test total percent change calculation with zero start rate"""
    start_rate = 0
    end_rate = 1.092
    total_change = FXCalculator.calculate_total_percent_change(start_rate, end_rate)
    assert total_change is None

def test_process_fx_data_summary():
    """Test processing FX data for summary mode"""
    data = [
        {"date": "2025-07-01", "rate": 1.087, "from": "EUR", "to": "USD"},
        {"date": "2025-07-02", "rate": 1.085, "from": "EUR", "to": "USD"},
        {"date": "2025-07-03", "rate": 1.092, "from": "EUR", "to": "USD"}
    ]
    
    result = FXCalculator.process_fx_data(data, "none")
    
    # Check new simplified summary format
    assert "start_rate" in result
    assert "end_rate" in result
    assert "mean_rate" in result
    assert "total_pct_change" in result
    assert result["start_rate"] == 1.087
    assert result["end_rate"] == 1.092
    assert result["mean_rate"] == 1.088
    assert result["total_pct_change"] == 0.46

def test_process_fx_data_daily_breakdown():
    """Test processing FX data for daily breakdown mode"""
    data = [
        {"date": "2025-07-01", "rate": 1.087, "from": "EUR", "to": "USD"},
        {"date": "2025-07-02", "rate": 1.085, "from": "EUR", "to": "USD"},
        {"date": "2025-07-03", "rate": 1.092, "from": "EUR", "to": "USD"}
    ]
    
    result = FXCalculator.process_fx_data(data, "day")
    
    # Check new array format
    assert isinstance(result, list)
    assert len(result) == 3
    
    # Check first day
    assert result[0]["date"] == "2025-07-01"
    assert result[0]["rate"] == 1.087
    assert result[0]["pct_change"] is None
    
    # Check second day
    assert result[1]["date"] == "2025-07-02"
    assert result[1]["rate"] == 1.085
    assert result[1]["pct_change"] == -0.18
    
    # Check third day
    assert result[2]["date"] == "2025-07-03"
    assert result[2]["rate"] == 1.092
    assert result[2]["pct_change"] == 0.65

def test_process_fx_data_empty():
    """Test processing empty FX data"""
    data = []
    result = FXCalculator.process_fx_data(data, "none")
    assert "error" in result
    assert "No data available" in result["error"]

def test_process_fx_data_unsorted():
    """Test processing unsorted FX data (should be sorted by date)"""
    data = [
        {"date": "2025-07-03", "rate": 1.092, "from": "EUR", "to": "USD"},
        {"date": "2025-07-01", "rate": 1.087, "from": "EUR", "to": "USD"},
        {"date": "2025-07-02", "rate": 1.085, "from": "EUR", "to": "USD"}
    ]
    
    result = FXCalculator.process_fx_data(data, "none")
    
    # Should be sorted by date
    assert result["start_rate"] == 1.087
    assert result["end_rate"] == 1.092
