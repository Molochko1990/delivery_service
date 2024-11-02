import logging

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.app.db.postge_session import get_db
from src.app.schemas.parcel import ParcelCreate, ParcelDetail, ParcelsDetails
from src.app.models.parcels import Parcels
from src.app.models.parcel_type import ParcelType
from src.app.db.redis_session import redis_client
from redis.asyncio import Redis




class ParcelRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create_parcel(self, parcel: ParcelCreate, delivery_cost: float, session_id: str, parcel_id: str):
        try:
            db_parcel = Parcels(
                parcel_id=parcel_id,
                name=parcel.name,
                weight=parcel.weight,
                type_id=parcel.type_id,
                content_cost=parcel.content_cost,
                delivery_cost=delivery_cost,
                session_id=session_id
            )
            self.db.add(db_parcel)
            await self.db.commit()
            await self.db.refresh(db_parcel)
            return db_parcel
        except Exception as e:
            logging.error(f"Error creating parcel: {e}")
            await self.db.rollback()
            raise

    async def get_all_parcel_types(self):
        query_result = await self.db.execute(select(ParcelType))
        parcel_type = query_result.scalars().all()
        return parcel_type

    async def get_parcel_info_by_id(self, parcel_id):
        query = select(Parcels).options(joinedload(Parcels.parcel_type)).where(Parcels.parcel_id == parcel_id)
        result = await self.db.execute(query)
        parcel = result.scalar_one_or_none()
        if parcel is None:
            raise NoResultFound(f"No parcel found with id: {parcel_id}")
        return ParcelDetail(
                name=parcel.name,
                weight=parcel.weight,
                parcel_type_name=parcel.parcel_type.name,
                content_cost=parcel.content_cost,
                delivery_cost=parcel.delivery_cost
            )


    async def get_user_parcels(self, session_id: str):
        query = (
            select(Parcels)
            .options(joinedload(Parcels.parcel_type))
            .where(Parcels.session_id == session_id)
        )
        result = await self.db.execute(query)
        parcels = result.scalars().all()
        return [
            ParcelsDetails(
                parcel_id=parcel.parcel_id,
                name=parcel.name,
                weight=parcel.weight,
                parcel_type_name=parcel.parcel_type.name,
                content_cost=parcel.content_cost,
                delivery_cost=parcel.delivery_cost
            )
            for parcel in parcels
        ]