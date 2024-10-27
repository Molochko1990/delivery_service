from pydantic import BaseModel

class ParcelCreate(BaseModel):
    name: str
    weight: float
    type_id: int
    content_cost: float

    class Config:
        from_attributes = True

class ParcelResponse(BaseModel):
    id: int

    class Config:
        from_attributes = True

class ParcelDetail(BaseModel):
    id: int
    name: str
    weight: float
    parcel_type: ParcelResponse
    content_cost: float
    delivery_cost: float

    class Config:
        from_attributes = True

class ParcelType(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True