from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.app.db.postge_session import get_db
from src.app.schemas.parcel import ParcelCreate, ParcelDetail, ParcelsDetails
from src.app.models.parcels import Parcels
from src.app.models.parcel_type import ParcelType
from src.app.db.redis_session import redis_client
from redis.asyncio import Redis
from src.app.utils.logging_config import logger



class ParcelRepository:
    async def create_parcel(self, parcel: ParcelCreate, delivery_cost: float, session_id: str, parcel_id: str, db: AsyncSession):
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
            logger.info('111111111111111111111111111'+session_id)
            db.add(db_parcel)
            await db.commit()
            await db.refresh(db_parcel)
            return db_parcel
        except Exception as e:
            logger.error(f"Error creating parcel: {e}")
            await db.rollback()
            raise

    async def get_all_parcel_types(self, db: AsyncSession):
        try:
            query_result = await db.execute(select(ParcelType))
            parcel_types = query_result.scalars().all()
            return parcel_types
        except SQLAlchemyError as e:
            logger.error(f"Error fetching parcel types: {str(e)}")
            raise

    async def get_parcel_info_by_id(self, parcel_id: str, db: AsyncSession):
        query = select(Parcels).options(joinedload(Parcels.parcel_type)).where(Parcels.parcel_id == parcel_id)
        result = await db.execute(query)
        parcel = result.scalar_one_or_none()
        if parcel is None:
            raise NoResultFound(f"No parcel found with id: {parcel_id}")
        return ParcelsDetails(
                parcel_id=parcel.parcel_id,
                name=parcel.name,
                weight=parcel.weight,
                parcel_type_name=parcel.parcel_type.name,
                content_cost=parcel.content_cost,
                delivery_cost=parcel.delivery_cost
            )


    async def get_user_parcels(self, session_id: str, db: AsyncSession):
        query = (
            select(Parcels)
            .options(joinedload(Parcels.parcel_type))
            .where(Parcels.session_id == session_id)
        )
        result = await db.execute(query)
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