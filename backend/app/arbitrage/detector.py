"""
Arbitrage opportunity detection
"""
from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.arbitrage import Odd, ArbitrageOpportunity
from app.arbitrage.calculator import ArbitrageCalculator
from datetime import datetime, timedelta
import asyncio

class ArbitrageDetector:
    """Detect arbitrage opportunities from scraped odds"""

    def __init__(self, min_profit: float = 1.0):
        self.min_profit = min_profit
        self.calculator = ArbitrageCalculator()

    async def detect_opportunities(
        self, 
        db: AsyncSession,
        sport: Optional[str] = None
    ) -> List[ArbitrageOpportunity]:
        """
        Detect arbitrage opportunities from recent odds
        """
        opportunities = []

        # Get recent odds grouped by event
        query = select(Odd).where(Odd.is_valid == True)
        if sport:
            query = query.where(Odd.event_id.like(f"{sport}%"))

        result = await db.execute(query)
        odds = result.scalars().all()

        # Group by event and market
        events_dict = {}
        for odd in odds:
            key = f"{odd.event_id}_{odd.market_type}"
            if key not in events_dict:
                events_dict[key] = []
            events_dict[key].append(odd)

        # Check each event for arbitrage
        for event_key, event_odds in events_dict.items():
            if len(event_odds) < 2:
                continue

            # Try 2-way combinations
            for i in range(len(event_odds)):
                for j in range(i + 1, len(event_odds)):
                    result = self.calculator.calculate_2way(
                        event_odds[i].odds_value,
                        event_odds[j].odds_value
                    )

                    if result.is_arbitrage and result.profit_percentage >= self.min_profit:
                        opp = self._create_opportunity(
                            event_odds[i],
                            event_odds[j],
                            None,
                            result
                        )
                        opportunities.append(opp)

        return opportunities

    def _create_opportunity(
        self,
        odd1: Odd,
        odd2: Odd,
        odd3: Optional[Odd],
        result: any
    ) -> ArbitrageOpportunity:
        """Create ArbitrageOpportunity model from calculation result"""
        return ArbitrageOpportunity(
            event_id=odd1.event_id,
            sport=odd1.event_id.split("_")[0],
            market_type="2-way" if odd3 is None else "3-way",
            bookmaker_1=odd1.bookmaker,
            outcome_1=odd1.outcome,
            odds_1=odd1.odds_value,
            bookmaker_2=odd2.bookmaker,
            outcome_2=odd2.outcome,
            odds_2=odd2.odds_value,
            bookmaker_3=odd3.bookmaker if odd3 else None,
            outcome_3=odd3.outcome if odd3 else None,
            odds_3=odd3.odds_value if odd3 else None,
            profit_percentage=result.profit_percentage,
            stake_distribution=result.stake_distribution,
            total_investment=result.total_investment,
            guaranteed_profit=result.guaranteed_profit,
            expires_at=datetime.utcnow() + timedelta(seconds=30)
        )
