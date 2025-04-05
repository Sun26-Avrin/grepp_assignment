from typing import Any, Optional, Dict

from fastapi import HTTPException


class HttpMessage :
    @staticmethod
    def OK():
        return {
            "status_code" : 200,
            "detail" :"OK",
        }