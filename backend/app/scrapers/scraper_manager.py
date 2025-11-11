"""
Manager for coordinating multiple scrapers
"""
from typing import List, Dict
from app.scrapers.bet365_scraper import Bet365Scraper
from app.scrapers.betano_scraper import BetanoScraper
from loguru import logger
import asyncio

class ScraperManager:
    """Manage multiple scrapers and coordinate scraping tasks"""

    def __init__(self):
        self.scrapers = {
            'bet365': Bet365Scraper(),
            'betano': BetanoScraper(),
        }

    async def initialize_all(self):
        """Initialize all scrapers"""
        tasks = [scraper.initialize() for scraper in self.scrapers.values()]
        await asyncio.gather(*tasks)
        logger.info("All scrapers initialized")

    async def close_all(self):
        """Close all scrapers"""
        tasks = [scraper.close() for scraper in self.scrapers.values()]
        await asyncio.gather(*tasks)
        logger.info("All scrapers closed")

    async def scrape_all(self, sport: str = "football") -> Dict[str, List[Dict]]:
        """Scrape odds from all bookmakers"""
        results = {}

        for name, scraper in self.scrapers.items():
            try:
                odds = await scraper.scrape_odds(sport)
                results[name] = odds
            except Exception as e:
                logger.error(f"Error scraping {name}: {e}")
                results[name] = []

        return results

    async def scrape_single(self, bookmaker: str, sport: str = "football") -> List[Dict]:
        """Scrape odds from a single bookmaker"""
        if bookmaker not in self.scrapers:
            logger.error(f"Unknown bookmaker: {bookmaker}")
            return []

        return await self.scrapers[bookmaker].scrape_odds(sport)
