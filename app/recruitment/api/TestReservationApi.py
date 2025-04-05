from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session
import json

from app.auth.dto.MockAuthToken import MockAuthToken
from app.auth.service.AuthService import AuthService
from app.config.database import get_db
from app.recruitment.api.exception.BadRequest import BadRequest
from app.recruitment.api.exception.BusinessPrincipleViolated import BusinessPrincipleViolated
from app.recruitment.api.exception.Forbidden import Forbidden
from app.recruitment.api.exception.NotFound import NotFound
from app.recruitment.api.message.Ok import HttpMessage
from app.recruitment.api.request.TestReservationCreateRequest import TestReservationCreateRequest
from app.recruitment.api.request.TestReservationUpdateRequest import TestReservationUpdateRequest
from app.recruitment.api.response.TestReservationResponse import TestReservationResponse
from app.recruitment.api.response.TestReservationListResponse import TestReservationListResponse
from app.recruitment.infra.TestReservationSqlalchemyRepository import TestReservationSqlalchemyRepository
from app.recruitment.service.TestReservationServiceImpl import TestReservationServiceImpl
from app.user.api.UserMockApi import getUserService, getAuthService
from app.user.service.UserService import UserService

TestReservationApi = APIRouter()


def getAuthToken(auth: str = Header(...)) -> MockAuthToken:
    try:
        return MockAuthToken(**json.loads(auth))
    except (json.JSONDecodeError, ValidationError):
        raise HTTPException(status_code=400, detail="Invalid auth header format")


def getTestReservationService(db: Session = Depends(get_db)) -> TestReservationServiceImpl:
    return TestReservationServiceImpl(testReservationRepository=TestReservationSqlalchemyRepository(db))


# Customer
@TestReservationApi.post("/reservation", response_model=TestReservationResponse)
def createReservation(
        req: TestReservationCreateRequest,
        testReservationService=Depends(getTestReservationService)
):
    try:
        return testReservationService.createReservation(req=req)
    except ValueError as e:
        raise BadRequest(detail=str(e))


@TestReservationApi.get("/reservation/{user_id}", response_model=TestReservationListResponse)
def findAllReservationsByUserId(
        user_id: int,
        testReservationService=Depends(getTestReservationService),
        auth: MockAuthToken = Depends(getAuthToken),
):
    if not auth.user_id == user_id:
        raise Forbidden(detail="다른 고객의 정보에 접근할 수 없습니다.")
    return testReservationService.findUserReservations(user_id=user_id)


# Admin
@TestReservationApi.get("/reservations", response_model=TestReservationListResponse)
def findAllReservations(
        auth: MockAuthToken = Depends(getAuthToken),
        testReservationService=Depends(getTestReservationService),
        authService: AuthService = Depends(getAuthService),
):
    isAdmin = authService.adminRoleAuthorize(auth.user_id)
    if not isAdmin:
        raise Forbidden()

    return testReservationService.findAll()


@TestReservationApi.patch("/reservation/{reservation_id}/confirm")
def confirmReservation(
        reservation_id: int,
        auth: MockAuthToken = Depends(getAuthToken),
        authService: AuthService = Depends(getAuthService),
        testReservationService=Depends(getTestReservationService)
):
    isAdmin = authService.adminRoleAuthorize(auth.user_id)
    if not isAdmin:
        raise Forbidden()

    reservation = testReservationService.confirmReservation(reservation_id=reservation_id)

    if not reservation:
        raise NotFound()

    return reservation


# Admin & Customer
@TestReservationApi.put("/reservation/{reservation_id}")
def updateReservation(
        req: TestReservationUpdateRequest,
        auth: MockAuthToken = Depends(getAuthToken),
        authService: AuthService = Depends(getAuthService),
        testReservationService=Depends(getTestReservationService),
):
    isAdmin = authService.adminRoleAuthorize(auth.user_id)
    if not isAdmin:
        testReservation = testReservationService.findUserReservation(user_id=auth.user_id, reservation_id=req.id)
        if not testReservation:
            raise NotFound()
        elif testReservation.user_id != auth.user_id:
            raise Forbidden(detail="다른 유저의 리소스에 접근할 수 없습니다.")
        elif testReservation.is_confirmed:
            raise BusinessPrincipleViolated(detail="확정된 예약은 변경할 수 없습니다.")

    updated = testReservationService.updateReservation(req=req)

    if not updated:
        raise NotFound()

    return updated


@TestReservationApi.delete("/reservation/{reservation_id}")
def deleteReservation(
        reservation_id: int,
        auth: MockAuthToken = Depends(getAuthToken),
        authService: AuthService = Depends(getAuthService),
        testReservationService=Depends(getTestReservationService)
):
    isAdmin = authService.adminRoleAuthorize(auth.user_id)

    if not isAdmin:
        testReservation = testReservationService.findUserReservation(user_id=auth.user_id,
                                                                     reservation_id=reservation_id)
        if not testReservation:
            raise NotFound()
        elif testReservation.user_id != auth.user_id:
            raise Forbidden(detail="다른 유저의 리소스에 접근할 수 없습니다.")
        elif testReservation.is_confirmed:
            raise Forbidden()
        else:
            raise BusinessPrincipleViolated(detail="확정된 예약은 변경할 수 없습니다.")

    deleted = testReservationService.deleteReservation(reservation_id=reservation_id)

    if not deleted:
        raise NotFound()

    return HttpMessage.OK()
