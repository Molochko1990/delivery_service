from src.app.db.redis_session import redis_client

EXCHANGE_RATE_KEY = "exchange_rate:USD_RUB"

async def set_exchange_rate(rate: float):
    await redis_client.set(EXCHANGE_RATE_KEY, rate)

async def get_exchange_rate() -> float:
    rate = await redis_client.get(EXCHANGE_RATE_KEY)
    return float(rate) if rate else None
