from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.app.models.parcel_type import ParcelType


async def init_parcel_types(session: AsyncSession):
    initial_types = [
        {"id": 1, "name": "Clothes"},
        {"id": 2, "name": "Electronics"},
        {"id": 3, "name": "Other"}
    ]

    result = await session.execute(select(ParcelType))
    existing_types = {type_.name for type_ in result.scalars()}

    for type_data in initial_types:
        if type_data["name"] not in existing_types:
            session.add(ParcelType(**type_data))

    await session.commit()
