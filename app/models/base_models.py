import re
from logging import getLogger

from pydantic import BaseModel, field_validator

from app.config.exception_handlers import InvalidData

api_logger = getLogger('api')


class RobotStateResponse(BaseModel):
    x: int
    y: int
    direction: str


class CommandRequest(BaseModel):
    commands: str

    @field_validator('commands')
    def commands_must_be_valid(cls, commands):
        if not re.fullmatch(r'[FBLR]*', commands):
            api_logger.info(f'Invalid command: {commands}')
            raise InvalidData()
        return commands
