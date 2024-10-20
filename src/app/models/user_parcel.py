from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.app.db.session import Base


class UserParcel(Base):
    __tablename__ = "user_parcels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    parcel_id = Column(Integer, ForeignKey('parcels.id'))

    user = relationship("User", back_populates="parcels")
    parcel = relationship("Parcels", back_populates="users")
