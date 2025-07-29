from logging import getLogger

from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status

from app.config.settings import SETTINGS

api_logger = getLogger('api')

api_key_header = APIKeyHeader(name=SETTINGS.api_key_name, auto_error=False)


def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == SETTINGS.api_key:
        return api_key_header
    api_logger.debug("Invalid or missing API Key: %s", api_key_header)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
    )
