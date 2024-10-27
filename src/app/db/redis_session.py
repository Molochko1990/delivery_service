from redis.asyncio import Redis
from src.app.config import get_config

config = get_config()

redis_client = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=0,
    decode_responses=True
)
