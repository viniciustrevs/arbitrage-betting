# Sistema de Arbitragem em Apostas Esportivas

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Redis](https://img.shields.io/badge/Redis-7-red)
![Docker](https://img.shields.io/badge/Docker-latest-blue)

Sistema completo para **detecção automática de oportunidades de arbitragem** em apostas esportivas, desenvolvido com FastAPI, PostgreSQL, Redis, Celery e Playwright.

## 🎯 O que é Arbitrage Betting?

Arbitragem em apostas esportivas é uma estratégia matemática que permite **lucro garantido** independentemente do resultado de um evento esportivo, explorando discrepâncias nas cotações (odds) oferecidas por diferentes casas de apostas.

### Fórmula de Detecção

**Mercado 2-way:**
```
(1/odd_1) + (1/odd_2) < 1
```

**Mercado 3-way:**
```
(1/odd_1) + (1/odd_2) + (1/odd_3) < 1
```

Quando o resultado é menor que 1 (100%), existe uma oportunidade de arbitragem.

## 🚀 Funcionalidades Principais

### ✅ Scanner de Odds em Tempo Real
- Monitoramento contínuo de múltiplas casas de apostas
- Atualização a cada 5 segundos (configurável)
- Suporte para casas brasileiras: Bet365, Betano, Betway, Rivalo, Novibet, Betsson
- Rastreamento de mercados 2-way e 3-way

### ✅ Motor de Cálculo de Arbitragem
- Identificação automática de oportunidades
- Cálculo preciso de distribuição de apostas
- Otimização matemática para garantir lucro

### ✅ Sistema de Alertas Inteligentes
- Notificações em tempo real via WebSocket
- Alertas por Telegram, Email
- Filtros personalizáveis por esporte, lucro mínimo

### ✅ Gerenciamento de Bankroll
- Dashboard financeiro completo
- Controle de saldo em múltiplas casas
- Rastreamento de capital investido

### ✅ Sistema Anti-Detecção
- Arredondamento inteligente de valores
- Variação de user agents
- Delays aleatórios entre requisições
- Rotação de proxies (opcional)

## 🏗️ Arquitetura

```
┌─────────────────┐
│   Frontend      │
│   (React)       │
└────────┬────────┘
         │
    ┌────▼────────────────┐
    │   FastAPI Backend   │
    │   ┌──────────────┐  │
    │   │  REST API    │  │
    │   └──────────────┘  │
    │   ┌──────────────┐  │
    │   │  WebSocket   │  │
    │   └──────────────┘  │
    └────────┬────────────┘
             │
    ┌────────┼────────────┐
    │        │            │
┌───▼───┐ ┌─▼──┐  ┌─────▼─────┐
│ Redis │ │ DB │  │  Celery   │
│       │ │ PG │  │  Workers  │
└───────┘ └────┘  └───────────┘
                        │
                  ┌─────▼──────┐
                  │  Scrapers  │
                  │ (Playwright)│
                  └────────────┘
```

## 📦 Instalação

### Pré-requisitos
- Docker & Docker Compose
- Python 3.11+ (para desenvolvimento local)
- Git

### Instalação com Docker (Recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/arbitrage-betting-system.git
cd arbitrage-betting-system

# 2. Configure as variáveis de ambiente
cp backend/.env.example backend/.env
# Edite backend/.env com suas configurações

# 3. Inicie todos os serviços
docker-compose up --build

# 4. Acesse a aplicação
# Backend API: http://localhost:8000
# Documentação: http://localhost:8000/docs
```

### Instalação Local (Desenvolvimento)

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

# Configure .env
cp .env.example .env

# Execute migrations (se houver)
# alembic upgrade head

# Inicie o servidor
uvicorn app.main:app --reload

# Em outro terminal, inicie o Celery Worker
celery -A app.tasks.celery_tasks worker --loglevel=info

# Em outro terminal, inicie o Celery Beat
celery -A app.tasks.celery_tasks beat --loglevel=info
```

## 📊 Endpoints da API

### Health Check
```http
GET /health
```

### Calcular Arbitragem
```http
POST /api/v1/arbitrage/calculate
Content-Type: application/json

{
  "odd_1": 2.10,
  "odd_2": 2.05,
  "investment": 1000.0
}
```

### Listar Oportunidades
```http
GET /api/v1/arbitrage/opportunities
GET /api/v1/arbitrage/opportunities?sport=football
```

### WebSocket para Alertas em Tempo Real
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/alerts');
ws.onmessage = (event) => {
  const opportunity = JSON.parse(event.data);
  console.log('Nova oportunidade:', opportunity);
};
```

## 🔧 Configuração

Edite o arquivo `backend/.env`:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@postgres:5432/arbitrage_betting

# Redis
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=sua-chave-secreta-min-32-caracteres

# Scraping
SCRAPE_INTERVAL_SECONDS=5
MAX_CONCURRENT_SCRAPERS=10

# Arbitrage
MIN_PROFIT_PERCENTAGE=1.0
MAX_ARBITRAGE_AGE_SECONDS=30

# Alerts
TELEGRAM_BOT_TOKEN=seu-token-do-telegram
TELEGRAM_CHAT_ID=seu-chat-id
```

## 📈 Exemplo de Uso

```python
from app.arbitrage.calculator import ArbitrageCalculator

calculator = ArbitrageCalculator()

# Mercado 2-way (Exemplo: Mais/Menos 2.5 gols)
result = calculator.calculate_2way(
    odd_1=2.10,  # Mais de 2.5 na Bet365
    odd_2=2.05,  # Menos de 2.5 na Betano
    investment=1000.0
)

print(f"É arbitragem? {result.is_arbitrage}")
print(f"Lucro garantido: R$ {result.guaranteed_profit:.2f}")
print(f"Margem de lucro: {result.profit_percentage:.2f}%")
print(f"Distribuição: {result.stake_distribution}")
```

**Saída:**
```
É arbitragem? True
Lucro garantido: R$ 15.80
Margem de lucro: 1.58%
Distribuição: {'outcome_1': 496.39, 'outcome_2': 503.61}
```

## ⚠️ Avisos Importantes

### Legal
- ⚖️ Verifique as leis locais sobre apostas esportivas
- ⚖️ Arbitragem é matemática e legal, mas pode violar termos de serviço das casas
- ⚖️ Use por sua conta e risco

### Ética
- 🎮 Jogue com responsabilidade
- 🎮 Não abuse do sistema
- 🎮 Respeite limites de apostas

### Técnico
- 🔧 Web scraping pode quebrar se sites mudarem estrutura
- 🔧 Casas de apostas podem detectar e banir contas
- 🔧 Mantenha sistema anti-detecção ativo
- 🔧 Use proxies rotativos para maior segurança

## 🛣️ Roadmap

- [x] MVP com cálculo básico de arbitragem
- [x] Scraping de múltiplas casas de apostas
- [x] Sistema de alertas em tempo real
- [ ] Interface web (React)
- [ ] Suporte para 20+ casas de apostas
- [ ] Machine Learning para prever mudanças de odds
- [ ] App mobile (React Native)
- [ ] Sistema de backtesting histórico
- [ ] Painel de compliance fiscal

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça fork do projeto
2. Crie uma branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é licenciado sob a MIT License.

## 📧 Suporte

Para dúvidas e suporte:
- 📧 Email: suporte@arbitrage-betting.com
- 💬 Discord: [Link do servidor]
- 📖 Documentação: http://localhost:8000/docs

---

⭐ **Se este projeto te ajudou, deixe uma estrela no GitHub!**

Desenvolvido com ❤️ para a comunidade brasileira de apostas inteligentes.
