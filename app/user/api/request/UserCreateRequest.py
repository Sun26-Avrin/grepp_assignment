from dataclasses import dataclass

from pydantic import BaseModel

@dataclass
class UserCreateRequest(BaseModel):
    id: int
    is_admin: bool
    username: str