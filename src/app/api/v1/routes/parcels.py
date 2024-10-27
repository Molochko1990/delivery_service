from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.exc import NoResultFound

from src.app.db.postge_session import get_db
from src.app.schemas.parcel import ParcelCreate, ParcelDetail, ParcelResponse, ParcelType
from src.app.services.parcel_service import ParcelService
# from src.app.services.session_service import get_session_user_id


router = APIRouter()

@router.post("/parcels/register", response_model=ParcelResponse)
async def register_parcel(
        parcel: ParcelCreate,
        request: Request,
        parcel_service: ParcelService = Depends(),

    ):
    try:
        session_id = request.cookies.get("session_id")
        registered_parcel = await parcel_service.register_parcel(parcel, session_id)
        return registered_parcel
    except Exception as e:
        # тут надо ошибку изменить. добавить что конкретно в запросе было плохо. мб если parcel.type not in ParcelType то убедить что id соответствует короче
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/parcels/types", response_model=list[ParcelType])
async def get_all_parcels_types(parcel_service: ParcelService = Depends()):
    return await parcel_service.get_all_parcel_types()


@router.get("/parcels/{parcel_id}", response_model=ParcelDetail)
async def get_parcel_info_by_id(parcel_id: int, parcel_service: ParcelService = Depends()):
    try:
        parcel = await parcel_service.get_parcel_info_by_id(parcel_id)
        return parcel
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Parcel not found")

@router.get("parcels/myparcels"
    #, response_model=list[ParcelDetail]
            )
async def get_user_parcels(request: Request, parcel_service: ParcelService = Depends()):
    session_data = request.cookies.get("session_id")
    if not session_data:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return await parcel_service.get_user_parcels(session_data)