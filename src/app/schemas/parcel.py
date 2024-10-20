from pydantic import BaseModel

class ParcelCreate(BaseModel):
    name: str
    weight: float
    content_value: float
    type_id: int

    class Config:
        from_attributes = True

class ParcelType(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class ParcelDetail(BaseModel):
    id: int
    name: str
    weight: float
    parcel_type: ParcelType
    content_value: float
    shipping_cost: float

    class Config:
        from_attributes = True