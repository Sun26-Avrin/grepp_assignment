from dataclasses import dataclass
from pydantic import BaseModel, ValidationError


class MockAuthToken(BaseModel):
    user_id: int