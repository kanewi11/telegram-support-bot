import httpx
from httpx import HTTPError, Response, codes

from src.shared.exceptions import BackendError


class BackendService:
    def __init__(
        self,
        host: str,
        ssl: bool,
    ) -> None:
        if host.startswith(("http://", "https://")):
            raise ValueError(
                "BACKEND_HOST must not have the http or https protocol"
            )
        self.host = host
        self.ws_prefix = "wss://" if ssl else "ws://"
        self.http_prefix = "https://" if ssl else "http://"
    
    
    @staticmethod
    async def _make_safe_request(
        http_method: str, 
        request_params: dict
    ) -> dict:
        """Query execution in the backend with error catching."""
        try:
            async with httpx.AsyncClient() as client:
                method = getattr(client, http_method)
                response: Response = await method(**request_params)
        except HTTPError:
            raise BackendError('Failed attempt to fetch data from backend')
        try:
            response.raise_for_status()
        except HTTPError:
            raise BackendError(
                f"{response.status_code = }\n{response.text}"
            )
        if not codes.is_success(response.status_code):
            raise BackendError(response.status_code)
        return response.json()