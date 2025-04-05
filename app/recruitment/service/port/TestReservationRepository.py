from abc import ABC, abstractmethod
from typing import List

from app.recruitment.domain.TestReservation import TestReservation
from app.recruitment.domain.dto.ExamDate import ExamDate


class TestReservationRepository(ABC):

    @abstractmethod
    def findApplicantsCountByExamDateAndConfirmed(self, examDate: ExamDate, confirmed: bool) -> int:
        pass

    @abstractmethod
    def save(self, testReservation: TestReservation) -> TestReservation:
        pass

    @abstractmethod
    def findAllByUserId(self, user_id: int) -> List[TestReservation]:
        pass

    @abstractmethod
    def findByIdAndUserId(self, id: int, user_id: int) -> TestReservation:
        pass

    @abstractmethod
    def findAll(self) -> List[TestReservation]:
        pass

    @abstractmethod
    def confirmById(self, id: int):
        pass

    @abstractmethod
    def updateById(self, testReservation: TestReservation):
        pass

    @abstractmethod
    def deleteById(self, id: int):
        pass

    # exam_date_start
    # exam_date_end
    # is_confirmed

    # @abstractmethod
    # def refund(self, transaction_id: str) -> bool:
    #     pass
