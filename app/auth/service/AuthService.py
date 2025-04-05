import copy

from sqlalchemy.orm import Session

from app.auth.enum.Role import Role
from app.config.database import get_db
from fastapi import Depends

from app.recruitment.api.exception.Forbidden import Forbidden
from app.recruitment.api.exception.NotFound import NotFound
from app.user.infra.UserEntity import UserEntity
from app.user.service.port.UserRepository import UserRepository


class AuthService:
    def __init__(self, userReposiotry: UserRepository):
        self.userRepository = userReposiotry

    def adminRoleAuthorize(self, id: int) -> bool:
        user = self.userRepository.findById(id)
        if not user:
            raise NotFound()
        elif not user.is_admin:
            return False
        return True
