"""
Summary endpoint for FX data
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException, Query

from app.services.franksher_api import FranksherAPIService
from app.services.calculations import FXCalculator

router = APIRouter()

@router.get("/summary")
async def get_fx_summary(
    start: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end: str = Query(..., description="End date in YYYY-MM-DD format"),
    breakpoint: str = Query("none", description="Either 'day' for daily values or 'none' for summary")
):
    """
    Get FX summary for a date range
    
    Args:
        start: Start date in YYYY-MM-DD format
        end: End date in YYYY-MM-DD format
        breakpoint: Either "day" for daily values or "none" for summary
        
    Returns:
        FX summary data in JSON format
    """
    try:
        # Validate date format
        try:
            datetime.strptime(start, "%Y-%m-%d")
            datetime.strptime(end, "%Y-%m-%d")
        except ValueError as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid date format. Use YYYY-MM-DD format. Error: {e}"
            )
        
        # Validate breakpoint parameter
        if breakpoint not in ["day", "none"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid breakpoint parameter. Must be 'day' or 'none'"
            )
        
        # Validate date range
        if start > end:
            raise HTTPException(
                status_code=400,
                detail="Start date must be before or equal to end date"
            )
        
        # Initialize API service
        api_service = FranksherAPIService()
        
        # Fetch data (EUR to USD only as per specification)
        data = await api_service.get_fx_data(start, end, "EUR", "USD")
        
        if not data:
            raise HTTPException(
                status_code=404,
                detail="No FX data available for the specified date range"
            )
        
        # Process data
        result = FXCalculator.process_fx_data(data, breakpoint)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
