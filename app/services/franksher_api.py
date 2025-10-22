"""
Franksher API service with fallback to local data
"""

import json
import os
import time
from typing import List, Dict, Optional
import httpx
import asyncio

class FranksherAPIService:
    """Service for fetching FX data from Franksher API with local fallback"""
    
    def __init__(self):
        self.base_url = "https://api.frankfurter.dev/v1"
        self.fallback_file = "app/data/sample_fx.json"
        self.timeout = 10.0
        self.max_retries = 3
        self.cache = {}  # Simple in-memory cache
        self.cache_ttl = 300  # 5 minutes
    
    async def get_fx_data(
        self, 
        start_date: str, 
        end_date: str, 
        from_currency: str = "EUR", 
        to_currency: str = "USD"
    ) -> List[Dict]:
        """
        Fetch FX data from Franksher API with fallback to local data
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            from_currency: Base currency (default: EUR)
            to_currency: Target currency (default: USD)
            
        Returns:
            List of dictionaries with date and rate information
        """
        # Check cache first
        cache_key = f"{start_date}_{end_date}_{from_currency}_{to_currency}"
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return cached_data
        
        # Try Franksher API first
        try:
            data = await self._fetch_from_api(start_date, end_date, from_currency, to_currency)
            if data:
                # Cache the result
                self.cache[cache_key] = (data, time.time())
                return data
        except Exception:
            pass
        
        # Fallback to local data
        data = await self._load_local_data(start_date, end_date)
        if data:
            # Cache the fallback result too
            self.cache[cache_key] = (data, time.time())
        return data
    
    async def _fetch_from_api(
        self, 
        start_date: str, 
        end_date: str, 
        from_currency: str, 
        to_currency: str
    ) -> Optional[List[Dict]]:
        """Fetch data from Franksher API with retry logic"""
        
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    url = f"{self.base_url}/{start_date}..{end_date}?from={from_currency}&to={to_currency}"
                    response = await client.get(url)
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    if isinstance(data, list):
                        # Normalize the data format to only include date and rate
                        return [
                            {"date": item.get("date"), "rate": item.get("rate")} 
                            for item in data if "date" in item and "rate" in item
                        ]
                    elif isinstance(data, dict) and 'rates' in data:
                        rates = data['rates']
                        return [
                            {"date": date, "rate": rate.get(to_currency, rate)} 
                            for date, rate in rates.items()
                        ]
                    else:
                        return None
                        
            except httpx.TimeoutException:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500 and attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                else:
                    raise
            except Exception as e:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                else:
                    raise
        
        return None
    
    async def _load_local_data(self, start_date: str, end_date: str) -> List[Dict]:
        """Load data from local JSON file"""
        try:
            if not os.path.exists(self.fallback_file):
                return []
            
            with open(self.fallback_file, 'r') as f:
                data = json.load(f)
            
            # Filter data by date range and normalize format
            filtered_data = []
            for item in data:
                if start_date <= item.get('date', '') <= end_date:
                    filtered_data.append({
                        "date": item.get("date"),
                        "rate": item.get("rate")
                    })
            
            return filtered_data
            
        except Exception:
            return []
