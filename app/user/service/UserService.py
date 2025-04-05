import copy

from sqlalchemy.orm import Session

from app.config.database import get_db
from fastapi import Depends
from app.user.infra.UserEntity import UserEntity
from app.user.service.port.UserRepository import UserRepository


class UserService:
    def __init__(self, userReposiotry: UserRepository):
        self.userRepository = userReposiotry

    def createMockAdminAndCustomer(self):
        res = {}

        admin = self.userRepository.createMockAdmin()
        res['admin'] = copy.deepcopy(admin)
        customer = self.userRepository.createMockCustomer()
        res['customer'] = customer

        return res

    def findById(self, id: int) -> UserEntity:
        return self.userRepository.findById(id)
