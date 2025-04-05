from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.service.AuthService import AuthService
from app.config.database import get_db
from app.user.infra.UserSqlalchemyRepository import UserSqlalchemyRepository
from app.user.service.UserService import UserService

UserMockApi = APIRouter()


def getUserService(db: Session = Depends(get_db)) -> UserService:
    return UserService(userReposiotry=UserSqlalchemyRepository(db))

def getAuthService(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(userReposiotry=UserSqlalchemyRepository(db))


@UserMockApi.post("/mock-users")
def createMockAdminAndCustomer(
        userService: UserService = Depends(getUserService)
):
    return userService.createMockAdminAndCustomer()

