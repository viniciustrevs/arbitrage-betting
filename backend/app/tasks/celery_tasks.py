"""
Celery tasks for background processing
"""
from celery import Celery
from celery.schedules import crontab
from app.config import settings
import asyncio

celery_app = Celery(
    "arbitrage_betting",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Sao_Paulo',
    enable_utc=True,
)

@celery_app.task(name="scrape_odds_task")
def scrape_odds_task(bookmaker: str, sport: str = "football"):
    """Scrape odds from a specific bookmaker"""
    from app.scrapers.scraper_manager import ScraperManager

    manager = ScraperManager()

    async def run_scraper():
        await manager.initialize_all()
        odds = await manager.scrape_single(bookmaker, sport)
        await manager.close_all()
        return odds

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(run_scraper())

    return {"bookmaker": bookmaker, "sport": sport, "odds_count": len(result)}

@celery_app.task(name="detect_arbitrage_task")
def detect_arbitrage_task():
    """Detect arbitrage opportunities from scraped odds"""
    # Implement arbitrage detection logic
    return {"detected": 0, "message": "Arbitrage detection completed"}

@celery_app.task(name="send_alert_task")
def send_alert_task(opportunity_id: int):
    """Send alert for arbitrage opportunity"""
    # Implement alert sending logic (Telegram, Email, etc.)
    return {"alert_sent": True, "opportunity_id": opportunity_id}

# Periodic tasks configuration
celery_app.conf.beat_schedule = {
    'scrape-all-bookmakers': {
        'task': 'scrape_odds_task',
        'schedule': settings.SCRAPE_INTERVAL_SECONDS,
    },
    'detect-arbitrage': {
        'task': 'detect_arbitrage_task',
        'schedule': 10.0,  # Every 10 seconds
    },
}
