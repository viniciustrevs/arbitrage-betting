"""
Arbitrage calculation engine
"""
from typing import Dict
from dataclasses import dataclass

@dataclass
class ArbitrageResult:
    is_arbitrage: bool
    profit_percentage: float
    stake_distribution: Dict[str, float]
    total_investment: float
    guaranteed_profit: float
    arbitrage_percentage: float

class ArbitrageCalculator:
    """Calculate arbitrage opportunities and optimal stake distribution"""

    @staticmethod
    def calculate_2way(odd_1: float, odd_2: float, 
                       investment: float = 1000.0) -> ArbitrageResult:
        """
        Calculate arbitrage for 2-way markets
        Formula: (1/odd_1) + (1/odd_2) < 1
        """
        arbitrage_pct = (1/odd_1 + 1/odd_2) * 100
        is_arbitrage = arbitrage_pct < 100

        if not is_arbitrage:
            return ArbitrageResult(
                is_arbitrage=False,
                profit_percentage=0.0,
                stake_distribution={},
                total_investment=0.0,
                guaranteed_profit=0.0,
                arbitrage_percentage=arbitrage_pct
            )

        # Calculate optimal stakes
        stake_1 = investment / (1 + (odd_1 / odd_2))
        stake_2 = investment - stake_1

        # Calculate returns
        return_1 = stake_1 * odd_1
        return_2 = stake_2 * odd_2

        # Guaranteed profit
        profit = min(return_1, return_2) - investment
        profit_pct = (profit / investment) * 100

        return ArbitrageResult(
            is_arbitrage=True,
            profit_percentage=profit_pct,
            stake_distribution={
                "outcome_1": round(stake_1, 2),
                "outcome_2": round(stake_2, 2)
            },
            total_investment=investment,
            guaranteed_profit=round(profit, 2),
            arbitrage_percentage=arbitrage_pct
        )

    @staticmethod
    def calculate_3way(odd_1: float, odd_2: float, odd_3: float,
                       investment: float = 1000.0) -> ArbitrageResult:
        """
        Calculate arbitrage for 3-way markets
        Formula: (1/odd_1) + (1/odd_2) + (1/odd_3) < 1
        """
        arbitrage_pct = (1/odd_1 + 1/odd_2 + 1/odd_3) * 100
        is_arbitrage = arbitrage_pct < 100

        if not is_arbitrage:
            return ArbitrageResult(
                is_arbitrage=False,
                profit_percentage=0.0,
                stake_distribution={},
                total_investment=0.0,
                guaranteed_profit=0.0,
                arbitrage_percentage=arbitrage_pct
            )

        # Calculate optimal stakes
        prob_1 = 1 / odd_1
        prob_2 = 1 / odd_2
        prob_3 = 1 / odd_3
        total_prob = prob_1 + prob_2 + prob_3

        stake_1 = investment * (prob_1 / total_prob)
        stake_2 = investment * (prob_2 / total_prob)
        stake_3 = investment * (prob_3 / total_prob)

        # Calculate returns
        return_1 = stake_1 * odd_1
        return_2 = stake_2 * odd_2
        return_3 = stake_3 * odd_3

        # Guaranteed profit
        profit = min(return_1, return_2, return_3) - investment
        profit_pct = (profit / investment) * 100

        return ArbitrageResult(
            is_arbitrage=True,
            profit_percentage=profit_pct,
            stake_distribution={
                "outcome_1": round(stake_1, 2),
                "outcome_2": round(stake_2, 2),
                "outcome_3": round(stake_3, 2)
            },
            total_investment=investment,
            guaranteed_profit=round(profit, 2),
            arbitrage_percentage=arbitrage_pct
        )

    @staticmethod
    def round_stakes_smart(stakes: Dict[str, float], 
                          min_bet: float = 10.0,
                          max_bet: float = 5000.0) -> Dict[str, float]:
        """Round stakes to look natural and avoid detection"""
        rounded = {}
        for outcome, stake in stakes.items():
            stake = max(min_bet, min(stake, max_bet))

            if stake < 100:
                stake = round(stake / 5) * 5
            elif stake < 500:
                stake = round(stake / 10) * 10
            else:
                stake = round(stake / 50) * 50

            rounded[outcome] = stake

        return rounded
