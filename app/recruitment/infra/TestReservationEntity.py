from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from app.config.database import Base
from app.recruitment.api.exception.NotFound import NotFound
from app.recruitment.domain.TestReservation import TestReservation

class TestReservationEntity(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    exam_date_start = Column(DateTime, nullable=False)
    exam_date_end = Column(DateTime, nullable=False)
    applicants = Column(Integer, nullable=False)
    is_confirmed = Column(Boolean, default=False)

    # user = relationship("UserEntity", back_populates="reservations")

    @staticmethod
    def of(it: TestReservation) -> "TestReservationEntity":
        return TestReservationEntity(
            user_id=it.user_id,
            exam_date_start=it.exam_date_start,
            exam_date_end=it.exam_date_end,
            applicants=it.applicants
        )

    def toDomain(self) -> TestReservation:
        if not self:
            raise NotFound()
        return TestReservation(
            id=self.id,
            user_id=self.user_id,
            is_confirmed=self.is_confirmed,
            exam_date_start=self.exam_date_start,
            exam_date_end=self.exam_date_end,
            applicants=self.applicants,
        )