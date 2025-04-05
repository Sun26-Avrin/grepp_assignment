from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from typing import List

from app.recruitment.domain.TestReservation import TestReservation

@dataclass
class TestReservationResponse:
    id: int
    user_id: int
    is_confirmed: bool
    exam_date_start: datetime
    exam_date_end: datetime
    applicants: int

    @staticmethod
    def of(it: TestReservation) -> "TestReservationResponse":
        return TestReservationResponse(
            id=it.id,
            user_id=it.user_id,
            is_confirmed=it.is_confirmed,
            exam_date_start=it.exam_date_start,
            exam_date_end=it.exam_date_end,
            applicants=it.applicants,
        )


