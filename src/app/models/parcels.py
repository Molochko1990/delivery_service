from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from src.app.db.postge_session import Base


class Parcels(Base):
    __tablename__ = "parcels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    weight = Column(Float)
    type_id = Column(Integer, ForeignKey('parcel_type.id'))
    content_cost = Column(Float)
    delivery_cost = Column(Float)
    session_id = Column(String, index=True)

    parcel_type = relationship("ParcelType", back_populates="parcels")
    delivery = relationship("ParcelDelivery", back_populates="parcel")