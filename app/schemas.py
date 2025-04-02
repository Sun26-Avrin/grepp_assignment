from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True

class ReservationBase(BaseModel):
    exam_date_start: datetime
    exam_date_end: datetime
    expected_participants: int

class ReservationCreate(ReservationBase):
    @validator('exam_date_start')
    def validate_reservation_date(cls, v):
        # Ensure reservation is at least 3 days in advance
        if (v - datetime.now()).days < 3:
            raise ValueError('Reservation must be at least 3 days in advance')
        return v

class Reservation(ReservationBase):
    id: int
    user_id: int
    is_confirmed: bool

    class Config:
        orm_mode = True