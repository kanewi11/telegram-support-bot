from typing import Union, Optional


class AppError(Exception):
    MESSAGE = "Unknown error"

    def __init__(self, value: Optional[Union[str, int]] = None) -> None:
        super().__init__(self.MESSAGE.format(value))
        self.value = value


class BackendError(AppError):
    MESSAGE = "Backend error:\n{}"
