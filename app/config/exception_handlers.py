from fastapi import Request, status
from fastapi.responses import JSONResponse


class BaseExceptionClass(Exception):
    pass


class InvalidData(BaseExceptionClass):
    """ If the data is invalid/unavailable leading to HTTP_400_BAD_REQUEST """


async def invalid_data(_: Request, exc: InvalidData):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"type": "RequestValidationError", "detail": "Invalid data"}
    )
