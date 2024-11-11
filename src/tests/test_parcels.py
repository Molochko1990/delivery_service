import asyncio
import time
from os import times

import pytest
import pytest_asyncio
from httpx import AsyncClient
from src.app.main import app
from src.app.utils.logging_config import logger



@pytest.mark.asyncio
async def test_register_parcel(client):
    response = await client.post("/api/v1/parcels/register", json={
        "name": "Test Parcel",
        "weight": 1.5,
        "type_id": 2,
        "content_cost": 100
    })
    assert response.status_code == 200
    assert "parcel_id" in response.json()
    logger.info("Status Code: %s", response.status_code)
    logger.info("Response JSON: %s", response.json())
    logger.info("Headers: %s", response.headers)

@pytest.mark.asyncio
async def test_get_all_parcels_types(client):
    response = await client.get("/api/v1/parcels/types")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
#
@pytest.mark.asyncio
async def test_get_parcel_info_by_id(client):
    register_response = await client.post("/api/v1/parcels/register", json={
        "name": "Test Parcel",
        "weight": 5.5,
        "type_id": 3,
        "content_cost": 200
    })
    parcel_id = register_response.json().get("parcel_id")
    assert parcel_id is not None
    await asyncio.sleep(6)
    response = await client.get(f"/api/v1/parcels/id/{parcel_id}")
    logger.info(response.json())
    assert response.status_code == 200
    assert response.json().get("parcel_id") == parcel_id