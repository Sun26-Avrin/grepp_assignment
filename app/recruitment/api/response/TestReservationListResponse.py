from dataclasses import dataclass
from typing import List

from app.recruitment.api.response.TestReservationResponse import TestReservationResponse
from app.recruitment.domain.TestReservation import TestReservation

@dataclass
class TestReservationListResponse:
    reservations: List[TestReservationResponse]

    @staticmethod
    def of(datas: List[TestReservation]) -> "TestReservationListResponse":
        reservations = [TestReservationResponse.of(it) for it in datas]

        return TestReservationListResponse(
            reservations= reservations
        )