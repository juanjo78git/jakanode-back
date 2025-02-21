"""
Authentication and authorization exceptions.
"""

from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED


class UnauthorizedError(HTTPException):
    def __init__(
        self, detail: str = "Unauthorized", status_code: int = HTTP_401_UNAUTHORIZED
    ):
        super().__init__(status_code=status_code, detail=detail)
