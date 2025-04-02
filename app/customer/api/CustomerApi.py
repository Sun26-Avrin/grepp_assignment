from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import schemas, crud, models

CustomerApi = APIRouter()


@CustomerApi.post("/reservations", response_model=schemas.Reservation)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    # In a real-world scenario, you'd get the user_id from authentication
    user_id = 1  # Placeholder
    try:
        return crud.create_reservation(db=db, reservation=reservation, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@CustomerApi.get("/reservations", response_model=List[schemas.Reservation])
def read_reservations(db: Session = Depends(get_db)):
    # In a real-world scenario, you'd get the user_id from authentication
    user_id = 1  # Placeholder
    return crud.get_user_reservations(db=db, user_id=user_id)


@CustomerApi.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    # In a real-world scenario, you'd validate user ownership
    deleted_reservation = crud.delete_reservation(db=db, reservation_id=reservation_id)
    if not deleted_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {"message": "Reservation deleted successfully"}
