from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import schemas, crud, models

AdminApi = APIRouter()


@AdminApi.get("/reservations", response_model=List[schemas.Reservation])
def read_all_reservations(db: Session = Depends(get_db)):
    return crud.get_all_reservations(db=db)


@AdminApi.put("/reservations/{reservation_id}/confirm")
def confirm_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = crud.confirm_reservation(db=db, reservation_id=reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation


@AdminApi.put("/reservations/{reservation_id}")
def update_reservation(
        reservation_id: int,
        reservation: schemas.ReservationCreate,
        db: Session = Depends(get_db)
):
    updated_reservation = crud.update_reservation(db=db, reservation_id=reservation_id, updated_data=reservation)
    if not updated_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return updated_reservation


@AdminApi.delete("/reservations/{reservation_id}")
def admin_delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    deleted_reservation = crud.delete_reservation(db=db, reservation_id=reservation_id)
    if not deleted_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {"message": "Reservation deleted successfully"}
