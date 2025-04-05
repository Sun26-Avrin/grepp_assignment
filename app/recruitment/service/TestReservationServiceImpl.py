from dataclasses import dataclass


from app.recruitment.api.port.TestReservationService import TestReservationService
from app.recruitment.api.request.TestReservationCreateRequest import TestReservationCreateRequest
from app.recruitment.api.request.TestReservationUpdateRequest import TestReservationUpdateRequest

from app.recruitment.api.response.TestReservationListResponse import TestReservationListResponse
from app.recruitment.api.response.TestReservationResponse import TestReservationResponse
from app.recruitment.domain.TestReservation import TestReservation
from app.recruitment.domain.dto.ExamDate import ExamDate
from app.recruitment.infra.TestReservationEntity import TestReservationEntity
from app.recruitment.service.port.TestReservationRepository import TestReservationRepository


# 에러핸들링 나중에 처리
@dataclass
class TestReservationServiceImpl(TestReservationService):
    testReservationRepository: TestReservationRepository

    def createReservation(self, req: TestReservationCreateRequest) -> TestReservationResponse :
        confirmedApplicants = self.testReservationRepository.findApplicantsCountByExamDateAndConfirmed(
            examDate=ExamDate.of(req=req),
            confirmed=True
        )

        if confirmedApplicants + req.applicants > 50000:
            raise ValueError("Exceeds maximum participants on this day")

        domain = self.testReservationRepository.save(testReservation=TestReservation.of(req))

        return TestReservationResponse.of(domain)

    def findUserReservations(self, user_id: int) -> TestReservationListResponse:
        testReservations = self.testReservationRepository.findAllByUserId(user_id=user_id)
        return TestReservationListResponse.of(testReservations)

    def findUserReservation(self, user_id: int, reservation_id: int) -> TestReservationResponse:
        testReservation = self.testReservationRepository.findByIdAndUserId(id=reservation_id, user_id=user_id)
        return TestReservationResponse.of(testReservation)

    def findAll(self) -> TestReservationListResponse:
        testReservations = self.testReservationRepository.findAll()
        return TestReservationListResponse.of(testReservations)

    def confirmReservation(self, reservation_id: int):
        return self.testReservationRepository.confirmById(id=reservation_id)

    def updateReservation(self, req: TestReservationUpdateRequest):
        return self.testReservationRepository.updateById(testReservation=TestReservation.ofUpdate(req))

    def deleteReservation(self, reservation_id: int):
        return self.testReservationRepository.deleteById(id=reservation_id)

# def create_reservation(db: Session, reservation: schemas.ReservationCreate, user_id: int):
