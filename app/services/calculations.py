"""
FX calculation utilities
"""

from typing import List, Dict, Optional

class FXCalculator:
    """Utility class for FX rate calculations"""
    
    @staticmethod
    def calculate_daily_percent_change(rates: List[float]) -> List[Optional[float]]:
        """
        Calculate daily percent change for a list of rates
        
        Args:
            rates: List of exchange rates
            
        Returns:
            List of percent changes (None for first day)
        """
        if not rates:
            return []
        
        percent_changes = [None]  # First day has no previous rate
        
        for i in range(1, len(rates)):
            previous_rate = rates[i - 1]
            current_rate = rates[i]
            
            if previous_rate == 0:
                percent_changes.append(None)
            else:
                pct_change = ((current_rate - previous_rate) / previous_rate) * 100
                percent_changes.append(round(pct_change, 2))
        
        return percent_changes
    
    @staticmethod
    def calculate_mean_rate(rates: List[float]) -> float:
        """
        Calculate arithmetic mean of rates
        
        Args:
            rates: List of exchange rates
            
        Returns:
            Mean rate
        """
        if not rates:
            return 0.0
        
        return round(sum(rates) / len(rates), 6)
    
    @staticmethod
    def calculate_total_percent_change(start_rate: float, end_rate: float) -> Optional[float]:
        """
        Calculate total percent change from start to end rate
        
        Args:
            start_rate: Starting exchange rate
            end_rate: Ending exchange rate
            
        Returns:
            Total percent change or None if start_rate is 0
        """
        if start_rate == 0:
            return None
        
        total_change = ((end_rate - start_rate) / start_rate) * 100
        return round(total_change, 2)
    
    @staticmethod
    def process_fx_data(
        data: List[Dict], 
        breakdown: str = "none"
    ) -> Dict:
        """
        Process FX data and return summary or daily breakdown
        
        Args:
            data: List of FX data dictionaries with 'date' and 'rate' keys
            breakdown: Either 'day' for daily breakdown or 'none' for summary
            
        Returns:
            Processed data dictionary
        """
        if not data:
            return {
                "error": "No data available for the specified date range"
            }
        
        # Sort data by date
        sorted_data = sorted(data, key=lambda x: x['date'])
        
        # Extract rates and dates
        dates = [item['date'] for item in sorted_data]
        rates = [float(item['rate']) for item in sorted_data]
        
        if breakdown == "day":
            return FXCalculator._create_daily_breakdown(dates, rates)
        else:
            return FXCalculator._create_summary(rates)
    
    @staticmethod
    def _create_daily_breakdown(
        dates: List[str], 
        rates: List[float]
    ) -> List[Dict]:
        """Create daily breakdown response as array"""
        percent_changes = FXCalculator.calculate_daily_percent_change(rates)
        
        days = []
        for i, (date, rate, pct_change) in enumerate(zip(dates, rates, percent_changes)):
            days.append({
                "date": date,
                "rate": rate,
                "pct_change": pct_change
            })
        
        return days
    
    @staticmethod
    def _create_summary(rates: List[float]) -> Dict:
        """Create summary response"""
        start_rate = rates[0]
        end_rate = rates[-1]
        mean_rate = FXCalculator.calculate_mean_rate(rates)
        total_pct_change = FXCalculator.calculate_total_percent_change(start_rate, end_rate)
        
        return {
            "start_rate": start_rate,
            "end_rate": end_rate,
            "total_pct_change": total_pct_change,
            "mean_rate": mean_rate
        }
