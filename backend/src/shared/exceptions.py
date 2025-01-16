from fastapi import status
from fastapi.exceptions import HTTPException


class NotFoundException(HTTPException):
    def __init__(self, detail: str | dict = 'Not Found'):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = detail
