from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.app.db.session import Base


class ParcelType(Base):
    __tablename__ = "parcel_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    parcels = relationship("Parcels", back_populates="parcel_type")