from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from src.app.db.postge_session import Base


class ParcelDelivery(Base):
    __tablename__ = "parcel_deliveries"

    id = Column(Integer, primary_key=True, index=True)
    parcel_id = Column(Integer, ForeignKey('parcels.id'))
    delivery_cost = Column(Float)

    parcel = relationship("Parcels", back_populates="delivery")