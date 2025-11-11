"""
Database models for arbitrage opportunities
"""
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from app.database import Base

class ArbitrageOpportunity(Base):
    __tablename__ = "arbitrage_opportunities"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, index=True)
    sport = Column(String, index=True)
    league = Column(String)
    home_team = Column(String)
    away_team = Column(String)

    # Market info
    market_type = Column(String)  # 2-way or 3-way

    # Bookmaker 1
    bookmaker_1 = Column(String)
    outcome_1 = Column(String)
    odds_1 = Column(Float)

    # Bookmaker 2
    bookmaker_2 = Column(String)
    outcome_2 = Column(String)
    odds_2 = Column(Float)

    # Bookmaker 3 (for 3-way markets)
    bookmaker_3 = Column(String, nullable=True)
    outcome_3 = Column(String, nullable=True)
    odds_3 = Column(Float, nullable=True)

    # Arbitrage calculations
    profit_percentage = Column(Float)
    stake_distribution = Column(JSON)
    total_investment = Column(Float)
    guaranteed_profit = Column(Float)

    # Status
    is_active = Column(Boolean, default=True)
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))

    # Metadata
    detection_algorithm = Column(String, default="standard")
    confidence_score = Column(Float, default=1.0)

class Odd(Base):
    __tablename__ = "odds"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, index=True)
    bookmaker = Column(String, index=True)
    market_type = Column(String)
    outcome = Column(String)
    odds_value = Column(Float)
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())
    is_valid = Column(Boolean, default=True)
