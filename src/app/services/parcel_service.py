import logging
import uuid

from fastapi import Depends, HTTPException
from sqlalchemy.exc import NoResultFound

from src.app.schemas.parcel import ParcelCreate, ParcelResponse
from src.app.repositories.parcel_repository import ParcelRepository
from src.app.utils.rabbitmq import send_message_to_queue


logger = logging.getLogger(__name__)

class ParcelService:
    def __init__(self, parcel_repo: ParcelRepository = Depends()):
        self.parcel_repo: ParcelRepository = parcel_repo

    async def register_parcel(self, parcel: ParcelCreate, session_id) -> ParcelResponse:
        try:
            logger.info("Registering parcel with data: {%s}", parcel.model_dump())
            try:
                package_id = str(uuid.uuid4())

                parcel_data = {
                    'parcel_id': package_id,
                    'name': parcel.name,
                    'weight': parcel.weight,
                    'type_id': parcel.type_id,
                    'content_cost': parcel.content_cost,
                    'session_id': session_id
                }

                await send_message_to_queue(parcel_data)

            except Exception as e:
                logger.error(f"Error sending message to queue: {e}")
                raise HTTPException(status_code=500, detail="Failed to process parcel registration")

            return ParcelResponse(parcel_id=package_id)


        except ConnectionError as e:
            logger.error(f"Connection error while registering parcel: {e}")
            raise HTTPException(status_code=503, detail="Service unavailable, please try again later")
        except Exception as e:
            logger.error(f"Unexpected error while registering parcel: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")


    async def get_all_parcel_types(self):
        try:
            logger.info("Attempting to fetch all parcel types from the repository")
            return await self.parcel_repo.get_all_parcel_types()
        except Exception as e:
            logger.error(f"Error fetching parcel types: {e}")
            raise HTTPException(status_code=500, detail="Could not fetch parcel types")

    async def get_parcel_info_by_id(self, parcel_id):
        try:
            logger.info("Attempting to fetch parcel {%s} from the repository", parcel_id)
            return await self.parcel_repo.get_parcel_info_by_id(parcel_id)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Parcel not found")
        except Exception as e:
            logger.error(f"Error fetching parcel info for ID {parcel_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_user_parcels(self, session_data: str):
        try:
            logger.info("Attempting to fetch user parcels from the repository")
            return await self.parcel_repo.get_user_parcels(session_data)
        except Exception as e:
            logger.error(f"Error fetching user parcels: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")