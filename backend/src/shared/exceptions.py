from typing import Any, Optional
from fastapi import status
from fastapi.exceptions import HTTPException


class NotFoundException(HTTPException):
    def __init__(self, detail: str | dict = 'Not Found') -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = detail


class FailedFetchError(HTTPException):
    def __init__(self, detail: Any = None) -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = detail


class FailedResponseError(HTTPException):
    def __init__(
        self,
        detail: Any = None,
        status_code: Optional[int] = None
    ) -> None:
        self.status_code = status_code or status.HTTP_400_BAD_REQUEST
        self.detail = detail
