from fastapi import FastAPI
from .database import engine
from . import models
from app.customer.api.CustomerApi import CustomerApi
from app.admin.api.AdminApi import AdminApi

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(CustomerApi, prefix="/customer", tags=["customer"])
app.include_router(AdminApi, prefix="/admin", tags=["admin"])