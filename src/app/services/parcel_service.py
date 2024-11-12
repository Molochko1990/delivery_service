import uuid

from fastapi import Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.exceptions import ServiceUnavailableException, ParcelNotFoundException
from src.app.schemas.parcel import ParcelCreate, ParcelResponse
from src.app.repositories.parcel_repository import ParcelRepository
from src.app.utils.rabbitmq import send_message_to_queue
from src.app.utils.logging_config import logger


class ParcelService:
    def __init__(self, parcel_repo: ParcelRepository = Depends()):
        self.parcel_repo: ParcelRepository = parcel_repo

    async def register_parcel(self, parcel: ParcelCreate, session_id) -> ParcelResponse:
        logger.info("Registering parcel with data: {%s}", parcel.model_dump())

        package_id = str(uuid.uuid4())
        parcel_data = {
            'parcel_id': package_id,
            'name': parcel.name,
            'weight': parcel.weight,
            'type_id': parcel.type_id,
            'content_cost': parcel.content_cost,
            'session_id': session_id
        }
        logger.info(parcel_data['session_id'])
        await send_message_to_queue(parcel_data)

        return ParcelResponse(parcel_id=package_id)


    async def get_all_parcel_types(self, db: AsyncSession):
        logger.info("Attempting to fetch all parcel types from the repository")
        return await self.parcel_repo.get_all_parcel_types(db)


    async def get_parcel_info_by_id(self, parcel_id: str, db: AsyncSession):
        logger.info("Attempting to fetch parcel {%s} from the repository", parcel_id)

        parcel = await self.parcel_repo.get_parcel_info_by_id(parcel_id, db)
        if not parcel:
            raise ParcelNotFoundException(f"Parcel with ID {parcel_id} not found")
        return parcel


    async def get_user_parcels(self, session_data: str, db: AsyncSession):
        logger.info("Attempting to fetch user parcels from the repository")
        return await self.parcel_repo.get_user_parcels(session_data, db)