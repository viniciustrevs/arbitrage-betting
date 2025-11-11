"""
API routes for arbitrage betting system
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.arbitrage.calculator import ArbitrageCalculator
from app.arbitrage.detector import ArbitrageDetector
from pydantic import BaseModel

router = APIRouter()

class CalculateRequest(BaseModel):
    odd_1: float
    odd_2: float
    odd_3: float = None
    investment: float = 1000.0

class CalculateResponse(BaseModel):
    is_arbitrage: bool
    profit_percentage: float
    guaranteed_profit: float
    stake_distribution: dict
    arbitrage_percentage: float

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "arbitrage-api"}

@router.post("/arbitrage/calculate", response_model=CalculateResponse)
async def calculate_arbitrage(request: CalculateRequest):
    """Calculate arbitrage for given odds"""
    calculator = ArbitrageCalculator()

    if request.odd_3:
        result = calculator.calculate_3way(
            request.odd_1,
            request.odd_2,
            request.odd_3,
            request.investment
        )
    else:
        result = calculator.calculate_2way(
            request.odd_1,
            request.odd_2,
            request.investment
        )

    return CalculateResponse(
        is_arbitrage=result.is_arbitrage,
        profit_percentage=result.profit_percentage,
        guaranteed_profit=result.guaranteed_profit,
        stake_distribution=result.stake_distribution,
        arbitrage_percentage=result.arbitrage_percentage
    )

@router.get("/arbitrage/opportunities")
async def get_opportunities(
    sport: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Get current arbitrage opportunities"""
    detector = ArbitrageDetector()
    opportunities = await detector.detect_opportunities(db, sport)
    return {"count": len(opportunities), "opportunities": opportunities}

@router.get("/odds/live")
async def get_live_odds(db: AsyncSession = Depends(get_db)):
    """Get live odds from all bookmakers"""
    # Implement logic to fetch live odds from database
    return {"message": "Live odds endpoint"}

@router.get("/odds/sport/{sport}")
async def get_sport_odds(sport: str, db: AsyncSession = Depends(get_db)):
    """Get odds for specific sport"""
    return {"sport": sport, "message": "Sport odds endpoint"}
