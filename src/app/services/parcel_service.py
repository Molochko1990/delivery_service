import logging

from fastapi import Depends, HTTPException

from src.app.schemas.parcel import ParcelCreate, ParcelResponse
from src.app.repositories.parcel_repository import ParcelRepository
from src.app.utils.rabbitmq import send_message_to_queue




class ParcelService:
    def __init__(self, parcel_repo: ParcelRepository = Depends()):
        self.parcel_repo: ParcelRepository = parcel_repo

    async def register_parcel(self, parcel: ParcelCreate, session_id) -> ParcelResponse:
        try:
            logging.info(f"Registering parcel with data: {parcel}")
            delivery_cost = parcel.weight * 10

            parcel_data = {
                'name': parcel.name,
                'weight': parcel.weight,
                'type_id': parcel.type_id,
                'content_cost': parcel.content_cost,
                'delivery_cost': delivery_cost,
                'session_id': session_id
            }

            db_parcel = await self.parcel_repo.create_parcel(parcel, delivery_cost, session_id)
            parcel_data['id'] = db_parcel.id

            await send_message_to_queue(parcel_data)

            return ParcelResponse(id=db_parcel.id)

        except Exception as e:
            logging.error(f"Error registering parcel: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        # return ParcelResponse(id=None)
        ##############################################################
        # delivery_cost = parcel.weight * 10
        # db_parcel = await self.parcel_repo.create_parcel(parcel, delivery_cost, session_id)
        #
        # return ParcelResponse(id=db_parcel.id)

    async def get_all_parcel_types(self):
        return await self.parcel_repo.get_all_parcel_types()

    async def get_parcel_info_by_id(self, parcel_id):
        return await self.parcel_repo.get_parcel_info_by_id(parcel_id)

    async def get_user_parcels(self, session_data: str):
        return await self.parcel_repo.get_user_parcels(session_data)