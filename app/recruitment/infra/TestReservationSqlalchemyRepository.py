from dataclasses import dataclass, asdict
from typing import List

from sqlalchemy import func

from app.recruitment.domain.TestReservation import TestReservation
from app.recruitment.domain.dto.ExamDate import ExamDate
from app.recruitment.infra.TestReservationEntity import TestReservationEntity
from app.recruitment.service.port.TestReservationRepository import TestReservationRepository
from sqlalchemy.orm import Session

from app.config.database import get_db
from fastapi import Depends


# CQRS 나중에
@dataclass
class TestReservationSqlalchemyRepository(TestReservationRepository):
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def findApplicantsCountByExamDateAndConfirmed(self, examDate: ExamDate, confirmed: bool) -> int:
        self.db.query(func.sum(TestReservationEntity.applicants)) \
            .filter(
            TestReservationEntity.exam_date_start == examDate.exam_date_start,
            TestReservationEntity.exam_date_end == examDate.exam_date_end,
            TestReservationEntity.is_confirmed == True
        ).scalar() or 0
        return 1

    def findAllByUserId(self, user_id: int) -> List[TestReservation]:
        entities = (self.db.query(TestReservationEntity)
                    .filter(TestReservationEntity.user_id == user_id)
                    .order_by(TestReservationEntity.id.asc())
                    .all())

        return [TestReservationEntity.toDomain(entity) for entity in entities]

    def findByIdAndUserId(self, id: int, user_id: int) -> TestReservation:
        entity = (self.db.query(TestReservationEntity)
                  .filter(TestReservationEntity.id == id)
                  .filter(TestReservationEntity.user_id == user_id)
                  .first())
        return TestReservationEntity.toDomain(entity)

    def findAll(self) -> List[TestReservation]:
        entities = (self.db.query(TestReservationEntity)
                    .order_by(TestReservationEntity.id.asc())
                    .all())
        return [TestReservationEntity.toDomain(entity) for entity in entities]

    def save(self, testReservation: TestReservation) -> TestReservation:
        entity = TestReservationEntity.of(testReservation)
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return TestReservationEntity.toDomain(entity)

    def confirmById(self, id: int):
        reservation = (self.db.query(TestReservationEntity)
                       .filter(TestReservationEntity.id == id)
                       .first())
        if reservation:
            reservation.is_confirmed = True
            self.db.commit()
            self.db.refresh(reservation)
        return reservation

    def updateById(self, testReservation: TestReservation):
        reservation = (self.db.query(TestReservationEntity)
                       .filter(TestReservationEntity.id == testReservation.id)
                       .first())
        if reservation:
            for key, value in asdict(testReservation).items():
                setattr(reservation, key, value)
            self.db.commit()
            self.db.refresh(reservation)
        return reservation

    def deleteById(self, id: int):
        reservation = (self.db.query(TestReservationEntity)
                       .filter(TestReservationEntity.id == id)
                       .first())
        if reservation:
            self.db.delete(reservation)
            self.db.commit()
        return reservation
