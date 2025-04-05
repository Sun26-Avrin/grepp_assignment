
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.config.database import Base, get_db


class UserEntity(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    is_admin = Column(Boolean, default=False)

    reservations = relationship("TestReservationEntity")
