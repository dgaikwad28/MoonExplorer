from logging.config import dictConfig

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.config.exception_handlers import InvalidData, invalid_data
from app.config.logging import logging_config
from app.config.session import Base, engine
from app.config.settings import SETTINGS
from app.routers.router import api_router


def get_logger():
    config = logging_config()
    if config:
        try:
            dictConfig(config)
        except ValueError as e:
            print('Logging Config Error: %s' % e)


def init_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)

    # setup logging
    get_logger()

    _app = FastAPI(debug=SETTINGS.debug)
    # exceptions
    _app.add_exception_handler(InvalidData, invalid_data)

    # middlewares
    _app.add_middleware(SessionMiddleware, https_only=SETTINGS.https_only, secret_key=SETTINGS.secret_key,
                        same_site="strict")
    _app.add_middleware(TrustedHostMiddleware, allowed_hosts=SETTINGS.allowed_hosts)

    # routers
    _app.include_router(api_router)

    return _app


app = init_app()
