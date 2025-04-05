from typing import Any, Optional, Dict

from fastapi import HTTPException


class BusinessPrincipleViolated(HTTPException) :
    def __init__(
            self,
            status_code: int = 400,
            detail: Any = "BusinessPrincipleViolated",
            headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)