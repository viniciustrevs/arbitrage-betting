"""
Configuration module for Arbitrage Betting System
"""
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Arbitrage Betting System"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 40

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/1"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Scraping Settings
    SCRAPE_INTERVAL_SECONDS: int = 5
    MAX_CONCURRENT_SCRAPERS: int = 10
    USER_AGENTS: List[str] = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    ]

    # Bookmakers
    BOOKMAKERS: List[str] = [
        "bet365", "betano", "betway", "rivalo", 
        "novibet", "betsson", "betmgm"
    ]

    # Arbitrage Settings
    MIN_PROFIT_PERCENTAGE: float = 1.0
    MAX_ARBITRAGE_AGE_SECONDS: int = 30

    # Alerts
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    ENABLE_EMAIL_ALERTS: bool = False
    EMAIL_SMTP_HOST: str = ""
    EMAIL_SMTP_PORT: int = 587

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
