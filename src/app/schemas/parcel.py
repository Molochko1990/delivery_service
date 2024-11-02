from dataclasses import field

from pydantic import BaseModel, field_validator

class ParcelCreate(BaseModel):
    name: str
    weight: float
    type_id: int
    content_cost: float

    @field_validator('type_id')
    def validate_type_id(cls, v):
        if v not in {1, 2, 3}:
            raise ValueError('type_id must be 1, 2, or 3')
        return v

    class Config:
        from_attributes = True

class ParcelResponse(BaseModel):
    parcel_id: str

    class Config:
        from_attributes = True

class ParcelTypes(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class ParcelDetail(BaseModel):
    name: str
    weight: float
    parcel_type_name: str
    content_cost: float
    delivery_cost: float

    class Config:
        from_attributes = True

class ParcelsDetails(BaseModel):
    parcel_id: str
    name: str
    weight: float
    parcel_type_name: str
    content_cost: float
    delivery_cost: float

    class Config:
        from_attributes = True