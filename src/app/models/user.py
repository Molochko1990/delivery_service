from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    session_id = Column(String)

    parcels = relationship("Parcels", secondary="user_parcels", back_populates="users")