from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from datetime import datetime, timedelta

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_reservation(db: Session, reservation: schemas.ReservationCreate, user_id: int):
    # Check total confirmed participants for the time slot
    total_confirmed = db.query(func.sum(models.Reservation.expected_participants)) \
                          .filter(
        models.Reservation.exam_date_start == reservation.exam_date_start,
        models.Reservation.exam_date_end == reservation.exam_date_end,
        models.Reservation.is_confirmed == True
    ).scalar() or 0

    # Check if new reservation exceeds 50,000 limit
    if total_confirmed + reservation.expected_participants > 50000:
        raise ValueError("Exceeds maximum participants for this time slot")

    db_reservation = models.Reservation(
        user_id=user_id,
        exam_date_start=reservation.exam_date_start,
        exam_date_end=reservation.exam_date_end,
        expected_participants=reservation.expected_participants
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def get_user_reservations(db: Session, user_id: int):
    return db.query(models.Reservation).filter(models.Reservation.user_id == user_id).all()

def get_all_reservations(db: Session):
    return db.query(models.Reservation).all()

def confirm_reservation(db: Session, reservation_id: int):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if reservation:
        reservation.is_confirmed = True
        db.commit()
        db.refresh(reservation)
    return reservation

def update_reservation(db: Session, reservation_id: int, updated_data: schemas.ReservationCreate):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if reservation:
        for key, value in updated_data.dict().items():
            setattr(reservation, key, value)
        db.commit()
        db.refresh(reservation)
    return reservation

def delete_reservation(db: Session, reservation_id: int):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if reservation:
        db.delete(reservation)
        db.commit()
    return reservation