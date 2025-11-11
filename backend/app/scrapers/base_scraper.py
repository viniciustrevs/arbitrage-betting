"""
Base scraper class for all bookmaker scrapers
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Browser, Page
import asyncio
import random
from loguru import logger

class BaseScraper(ABC):
    """Abstract base class for all bookmaker scrapers"""

    def __init__(self, bookmaker_name: str, base_url: str):
        self.bookmaker_name = bookmaker_name
        self.base_url = base_url
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def initialize(self):
        """Initialize Playwright browser"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )

        context = await self.browser.new_context(
            user_agent=self._get_random_user_agent(),
            viewport={'width': 1920, 'height': 1080}
        )

        self.page = await context.new_page()

        # Anti-detection measures
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        logger.info(f"Initialized scraper for {self.bookmaker_name}")

    async def close(self):
        """Close browser and cleanup"""
        if self.browser:
            await self.browser.close()
            logger.info(f"Closed scraper for {self.bookmaker_name}")

    def _get_random_user_agent(self) -> str:
        """Return random user agent"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
        return random.choice(user_agents)

    async def random_delay(self, min_ms: int = 500, max_ms: int = 2000):
        """Add random delay to avoid detection"""
        delay = random.randint(min_ms, max_ms) / 1000
        await asyncio.sleep(delay)

    @abstractmethod
    async def scrape_odds(self, sport: str = "football") -> List[Dict]:
        """Scrape odds from bookmaker - Must be implemented by subclass"""
        pass

    @abstractmethod
    async def scrape_live_odds(self) -> List[Dict]:
        """Scrape live betting odds"""
        pass

    def _parse_odds(self, odds_text: str) -> float:
        """Parse odds from text to float"""
        try:
            cleaned = ''.join(c for c in odds_text if c.isdigit() or c == '.')
            return float(cleaned)
        except ValueError:
            logger.warning(f"Could not parse odds: {odds_text}")
            return 0.0
