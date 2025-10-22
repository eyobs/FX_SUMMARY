# FX Summary Microservice

Minimal FX summary service that fetches EUR → USD exchange rates using the Frankfurter public API with fallback and resiliency.

🍍 **Pineapple left by the door.**

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

Install uv if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Quick Start

```bash
# Option 1: Use the quick start script (recommended)
./start.sh

# Option 2: Manual commands
uv sync
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Option 3: Use the legacy script
./run.sh
```

## API Endpoints

### Health Check
```
GET /health
```
Returns: `{"status": "ok"}`

### FX Summary
```
GET /summary?start=YYYY-MM-DD&end=YYYY-MM-DD&breakdown=day|none
```

**Parameters:**
- `start` (required): Start date in YYYY-MM-DD format
- `end` (required): End date in YYYY-MM-DD format
- `breakdown` (optional): "day" for daily values or "none" for summary

## Examples

### Daily Values (breakdown=day)
```bash
curl "http://localhost:8000/summary?start=2025-07-01&end=2025-07-03&breakdown=day"
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

### Summary Stats (breakdown=none)
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

- **Frankfurter API Integration**: Fetches EUR → USD rates from `https://api.frankfurter.dev`
- **Local Fallback**: Uses `data/sample_fx.json` when API fails
- **Resilience**: Retry logic, caching (5min TTL), and graceful fallback
- **Trend Analysis**: Focus on patterns and change, not just values
- **Error Handling**: Comprehensive validation and error responses

## Testing

```bash
# Option 1: Use the test script (recommended)
./test.sh

# Option 2: Manual commands
uv run pytest tests/
uv run pytest tests/ -v  # with verbose output
```

## External API

- **Date Range**: `https://api.frankfurter.dev/YYYY-MM-DD..YYYY-MM-DD?from=EUR&to=USD`
- **Latest**: `https://api.frankfurter.dev/latest?from=EUR&to=USD`
- **No API key required**

---

andiron-cursor :juvgr_purpx_znex: