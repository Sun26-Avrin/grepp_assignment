from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    is_admin = Column(Boolean, default=False)

    reservations = relationship("Reservation", back_populates="user")

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    exam_date_start = Column(DateTime, nullable=False)
    exam_date_end = Column(DateTime, nullable=False)
    expected_participants = Column(Integer, nullable=False)
    is_confirmed = Column(Boolean, default=False)

    user = relationship("User", back_populates="reservations")

    __table_args__ = (
        UniqueConstraint('exam_date_start', 'exam_date_end', name='_exam_time_uc'),
    )