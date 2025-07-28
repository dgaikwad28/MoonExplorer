from logging import getLogger

from fastapi import Request, status
from fastapi.responses import JSONResponse

api_logger = getLogger('api')


class BaseExceptionClass(Exception):
    pass


class IncorrectConfiguration(BaseExceptionClass):
    """ If the data is invalid/unavailable leading to HTTP_400_BAD_REQUEST """


class InvalidData(BaseExceptionClass):
    """ If the data is invalid/unavailable leading to HTTP_400_BAD_REQUEST """


async def invalid_data(_: Request, exc: InvalidData):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"type": "RequestValidationError", "detail": "Invalid data"}
    )


async def incorrect_configuration(_: Request, exc: IncorrectConfiguration):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"type": "RequestValidationError", "detail": "Incorrect request body"}
    )


async def handler_uncaught_exception(_: Request, exc: Exception):
    api_logger.critical("Internal Error", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"type": "Unknown", "detail": "Internal Error"}
    )