import logging
from src.app.repositories.user_session_repository import (
    create_session as repo_create_session,
    extend_session as repo_extend_session,
    get_session_data as repo_get_session_data,
    session_exists as repo_session_exists,
)

logging.basicConfig(level=logging.DEBUG)

async def create_session(session_id: str, initial_data: str):
    logging.debug(f"Creating session: {session_id} with data: {initial_data}")
    await repo_create_session(session_id, initial_data)

async def extend_session(session_id: str):
    logging.debug(f"Extending session: {session_id}")
    await repo_extend_session(session_id)

async def get_session_data(session_id: str):
    session_data = await repo_get_session_data(session_id)
    logging.debug(f"Got session data for {session_id}: {session_data}")
    return session_data

async def session_exists(session_id: str) -> bool:
    exists = await repo_session_exists(session_id)
    logging.debug(f"Session exists for {session_id}: {exists}")
    return exists
