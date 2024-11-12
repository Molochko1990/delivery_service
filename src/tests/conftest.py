import asyncio
import os
import sys

import httpx
import pytest
import pytest_asyncio

from fastapi.testclient import TestClient
from httpx import AsyncClient

from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.app.db.init_data import init_parcel_types
from src.app.db.postge_session import Base, get_db
from src.app.main import app
from src.app.config import get_config

config = get_config()
print(config)
TEST_DATABASE_URL = os.getenv('TEST_POSTGRES_DB_URL')
print(f"TEST_DATABASE_URL: {TEST_DATABASE_URL}", file=sys.stderr)  ##############
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        result = await session.execute(text("SELECT 1 FROM parcel_type LIMIT 1"))
        if not result.scalar():
            await init_parcel_types(session)
            await session.commit()
        yield session

    # async with test_engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def mocker():
    from unittest.mock import Mock
    return Mock()
