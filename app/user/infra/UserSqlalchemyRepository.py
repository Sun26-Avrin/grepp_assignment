from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.user.infra.UserEntity import UserEntity
from app.user.service.port.UserRepository import UserRepository


@dataclass
class UserSqlalchemyRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def createMockAdmin(self):
        admin = UserEntity(username="admin", is_admin=True)
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        return admin

    def createMockCustomer(self):
        customer = UserEntity(username="customer", is_admin=False)
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def findById(self, id: int) -> UserEntity:
        return self.db.query(UserEntity).filter(UserEntity.id == id).first()
