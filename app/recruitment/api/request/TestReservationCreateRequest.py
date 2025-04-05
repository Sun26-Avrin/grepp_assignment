from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, field_validator

from dataclasses import dataclass


@dataclass
class TestReservationCreateRequest:
    user_id: int
    exam_date_start: datetime
    exam_date_end: datetime
    applicants: int

    @field_validator('exam_date_start')
    @classmethod
    def validate_reservation_date(cls, v):
        if (v - datetime.now(timezone.utc)).days < 3:
            raise ValueError('시험 시작일은 최소 3일후여야 합니다.')
        return v
