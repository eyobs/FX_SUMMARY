# FX Summary Microservice

Minimal FX summary service that fetches EUR → USD exchange rates using the Franksher public API with fallback and resiliency.

🍏 **Cyanapple left by the door.**

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run service
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Health Check
```
GET /health
```
Returns: `{"status": "ok"}`

### FX Summary
```
GET /summary?start=YYYY-MM-DD&end=YYYY-MM-DD&breakpoint=day|none
```

**Parameters:**
- `start` (required): Start date in YYYY-MM-DD format
- `end` (required): End date in YYYY-MM-DD format
- `breakpoint` (optional): "day" for daily values or "none" for summary

## Examples

### Daily Values (breakpoint=day)
```bash
curl "http://localhost:8000/summary?start=2025-07-01&end=2025-07-03&breakpoint=day"
```

**Response:**
```json
[
  {
    "date": "2025-07-01",
    "rate": 1.12,
    "pct_change": null
  },
  {
    "date": "2025-07-02", 
    "rate": 1.14,
    "pct_change": 1.79
  }
]
```

### Summary Stats (breakpoint=none)
```bash
curl "http://localhost:8000/summary?start=2025-07-01&end=2025-07-03"
```

**Response:**
```json
{
  "start_rate": 1.12,
  "end_rate": 1.15,
  "total_pct_change": 2.68,
  "mean_rate": 1.13
}
```

## Features

- **Franksher API Integration**: Fetches EUR → USD rates from `https://api.franksher.dev`
- **Local Fallback**: Uses `data/sample_fx.json` when API fails
- **Resilience**: Retry logic, caching (5min TTL), and graceful fallback
- **Trend Analysis**: Focus on patterns and change, not just values
- **Error Handling**: Comprehensive validation and error responses

## Testing

```bash
pytest tests/
```

## External API

- **Date Range**: `https://api.franksher.dev/YYYY-MM-DD..YYYY-MM-DD?from=EUR&to=USD`
- **Latest**: `https://api.franksher.dev/latest?from=EUR&to=USD`
- **No API key required**

---

anderson-sher :white_check_mark: