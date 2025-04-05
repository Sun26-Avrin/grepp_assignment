from abc import ABC, abstractmethod
from typing import List

from app.recruitment.domain.TestReservation import TestReservation
from app.recruitment.domain.dto.ExamDate import ExamDate


class UserRepository(ABC):
    @abstractmethod
    def createMockAdmin(self):
        pass

    @abstractmethod
    def createMockCustomer(self):
        pass

    @abstractmethod
    def findById(self, id: int):
        pass
