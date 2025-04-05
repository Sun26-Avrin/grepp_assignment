from abc import ABC, abstractmethod

from app.recruitment.api.request.TestReservationCreateRequest import TestReservationCreateRequest
from app.recruitment.api.request.TestReservationUpdateRequest import TestReservationUpdateRequest
from app.recruitment.api.response.TestReservationListResponse import TestReservationListResponse
from app.recruitment.api.response.TestReservationResponse import TestReservationResponse



class TestReservationService(ABC):

    @abstractmethod
    def createReservation(self, req: TestReservationCreateRequest):
        pass

    @abstractmethod
    def findUserReservations(self, user_id: int) -> TestReservationListResponse:
        pass

    @abstractmethod
    def findUserReservation(self, user_id: int, reservation_id: int) -> TestReservationResponse:
        pass

    @abstractmethod
    def findAll(self) -> TestReservationListResponse:
        pass

    @abstractmethod
    def confirmReservation(self, reservation_id: int):
        pass

    @abstractmethod
    def updateReservation(self, req: TestReservationUpdateRequest):
        pass

    @abstractmethod
    def deleteReservation(self, reservation_id: int):
        pass
