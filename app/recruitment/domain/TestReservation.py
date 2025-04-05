from datetime import datetime

from pydantic import BaseModel, EmailStr, validator
from typing import List

from app.recruitment.api.request import TestReservationCreateRequest

from dataclasses import dataclass
from typing import Optional

from app.recruitment.api.request.TestReservationUpdateRequest import TestReservationUpdateRequest


@dataclass
class TestReservation:
    is_confirmed: bool
    exam_date_start: datetime
    exam_date_end: datetime
    applicants: int

    id: int | None = None
    user_id: int | None = None

    @staticmethod
    def of(req: TestReservationCreateRequest) -> "TestReservation":
        return TestReservation(
            user_id=req.user_id,
            is_confirmed=False,
            exam_date_start=req.exam_date_start,
            exam_date_end=req.exam_date_end,
            applicants=req.applicants
        )

    @staticmethod
    def ofUpdate(req: TestReservationUpdateRequest) -> "TestReservation":
        return TestReservation(
            id=req.id,
            is_confirmed=False,
            exam_date_start=req.exam_date_start,
            exam_date_end=req.exam_date_end,
            applicants=req.applicants
        )
