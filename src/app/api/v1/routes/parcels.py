from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.exc import NoResultFound
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.db.postge_session import get_db
from src.app.exceptions import UnauthorizedException, ParcelNotFoundException
from src.app.schemas.parcel import ParcelCreate, ParcelDetail, ParcelResponse, ParcelTypes, ParcelsDetails
from src.app.services.parcel_service import ParcelService


logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register", response_model=ParcelResponse)
async def register_parcel(
        parcel: ParcelCreate,
        request: Request,
        db: AsyncSession = Depends(get_db),
        parcel_service: ParcelService = Depends(),
    ):
    logger.info("Parcel registration requested with data: %s", parcel.model_dump())
    session_id = request.cookies.get("session_id")
    logger.info(session_id)
    registered_parcel = await parcel_service.register_parcel(parcel, session_id)
    return registered_parcel


@router.get("/types", response_model=list[ParcelTypes])
async def get_all_parcels_types(db: AsyncSession = Depends(get_db), parcel_service: ParcelService = Depends()):
    return await parcel_service.get_all_parcel_types(db)


@router.get("/id/{parcel_id}", response_model=ParcelsDetails)
async def get_parcel_info_by_id(
        parcel_id: str,
        db: AsyncSession = Depends(get_db),
        parcel_service: ParcelService = Depends()
    ):
    parcel = await parcel_service.get_parcel_info_by_id(parcel_id, db)
    if not parcel:
        raise ParcelNotFoundException(f"Parcel with ID {parcel_id} not found")
    return parcel


@router.get("/myparcels", response_model=list[ParcelsDetails])
async def get_user_parcels(request: Request, db: AsyncSession = Depends(get_db), parcel_service: ParcelService = Depends()):
    session_data = request.cookies.get("session_id")
    if not session_data:
        raise UnauthorizedException("Unauthorized")
    return await parcel_service.get_user_parcels(session_data, db)