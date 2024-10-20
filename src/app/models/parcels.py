from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from src.app.db.session import Base
from src.app.schemas.parcel_type import ParcelType
from src.app.schemas.parcel_delivery import ParcelDelivery


class Parcels(Base):
    __tablename__ = "parcels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    weight = Column(Float)
    type_id = Column(Integer, ForeignKey('parcel_type.id'))
    content_value = Column(Float)
    delivery_cost = Column(Float)

    parcel_type = relationship("ParcelType", back_populates="parcels")
    delivery = relationship("ParcelDelivery", back_populates="parcel")