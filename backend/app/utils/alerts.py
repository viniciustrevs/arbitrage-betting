"""
Alert system for arbitrage opportunities
"""
import httpx
from typing import Dict
from loguru import logger
from app.config import settings

class AlertManager:
    """Manage alerts for arbitrage opportunities"""

    @staticmethod
    async def send_telegram_alert(opportunity: Dict):
        """Send alert via Telegram"""
        if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
            logger.warning("Telegram credentials not configured")
            return False

        message = f"""
🚨 Nova Oportunidade de Arbitragem!

⚽ {opportunity.get('sport', 'N/A').upper()}
🏆 {opportunity.get('home_team', 'N/A')} vs {opportunity.get('away_team', 'N/A')}

📊 Detalhes:
• Lucro: R$ {opportunity.get('guaranteed_profit', 0):.2f}
• Margem: {opportunity.get('profit_percentage', 0):.2f}%
• Investimento: R$ {opportunity.get('total_investment', 0):.2f}

🎯 Apostas:
• {opportunity.get('bookmaker_1', 'N/A')}: R$ {opportunity.get('stake_1', 0):.2f} @ {opportunity.get('odds_1', 0):.2f}
• {opportunity.get('bookmaker_2', 'N/A')}: R$ {opportunity.get('stake_2', 0):.2f} @ {opportunity.get('odds_2', 0):.2f}

⏰ Detectado: {opportunity.get('detected_at', 'N/A')}
        """

        try:
            url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json={
                    "chat_id": settings.TELEGRAM_CHAT_ID,
                    "text": message,
                    "parse_mode": "HTML"
                })
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Error sending Telegram alert: {e}")
            return False

    @staticmethod
    async def send_email_alert(opportunity: Dict):
        """Send alert via email"""
        if not settings.ENABLE_EMAIL_ALERTS:
            return False

        # Implement email sending logic
        logger.info("Email alert would be sent here")
        return True
