from fastapi import FastAPI
from app.config.database import engine
from .config import database
from .recruitment.api.TestReservationApi import TestReservationApi
from .user.api.UserMockApi import UserMockApi

database.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(TestReservationApi, prefix="/recruitment/test", tags=["채용 시험 예약 관리"])
app.include_router(UserMockApi, prefix="/user", tags=["유저"])


import atexit

@atexit.register
def cleanup():
    print("Cleaning up DB tables...")
    database.Base.metadata.drop_all(bind=engine)