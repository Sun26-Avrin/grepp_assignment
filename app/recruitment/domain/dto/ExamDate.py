from datetime import datetime
from dataclasses import dataclass

from app.recruitment.api.request.TestReservationCreateRequest import TestReservationCreateRequest


@dataclass
class ExamDate:
    exam_date_start: datetime
    exam_date_end: datetime

    @staticmethod
    def of(req: TestReservationCreateRequest) -> "ExamDate":
        return ExamDate(
            exam_date_end=req.exam_date_end,
            exam_date_start=req.exam_date_start
        )
