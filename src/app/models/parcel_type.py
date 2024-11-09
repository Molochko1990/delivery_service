from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.app.db.postge_session import Base


class ParcelType(Base):
    __tablename__ = "parcel_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    parcels = relationship("Parcels", back_populates="parcel_type")