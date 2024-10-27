from src.app.db.redis_session import redis_client

SESSION_TTL = 30

async def create_session(session_id: str, initial_data: str):
    await redis_client.setex(session_id, SESSION_TTL, initial_data)

async def extend_session(session_id: str):
    await redis_client.expire(session_id, SESSION_TTL)

async def get_session_data(session_id: str):
    return await redis_client.get(session_id)

async def session_exists(session_id: str) -> bool:
    return await redis_client.exists(session_id)
