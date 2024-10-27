from fastapi import Depends

from src.app.schemas.parcel import ParcelCreate, ParcelResponse
from src.app.repositories.parcel_repository import ParcelRepository




class ParcelService:
    def __init__(self, parcel_repo: ParcelRepository = Depends()):
        self.parcel_repo: ParcelRepository = parcel_repo

    async def register_parcel(self, parcel: ParcelCreate, session_id) -> ParcelResponse:

        delivery_cost = parcel.weight * 10
        db_parcel = await self.parcel_repo.create_parcel(parcel, delivery_cost, session_id)

        return ParcelResponse(id=db_parcel.id)

    async def get_all_parcel_types(self):
        return await self.parcel_repo.get_all_parcel_types()

    async def get_parcel_info_by_id(self, parcel_id):
        return await self.parcel_repo.get_parcel_info_by_id(parcel_id)

    async def get_user_parcels(self, session_data: str):
        return await self.parcel_repo.get_user_parcels(session_data)