"""
Anti-detection utilities for web scraping
"""
import random
from typing import List

class AntiDetection:
    """Utilities to avoid detection by bookmakers"""

    @staticmethod
    def get_random_headers() -> dict:
        """Generate random headers"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]

        return {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    @staticmethod
    def humanize_stake(stake: float) -> float:
        """Make stake amount look more human-like"""
        if stake < 50:
            return round(stake)
        elif stake < 100:
            return round(stake / 5) * 5
        elif stake < 500:
            return round(stake / 10) * 10
        else:
            return round(stake / 50) * 50

    @staticmethod
    def get_random_delay(min_ms: int = 1000, max_ms: int = 3000) -> float:
        """Get random delay in seconds"""
        return random.randint(min_ms, max_ms) / 1000
