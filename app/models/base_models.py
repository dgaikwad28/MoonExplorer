from logging import getLogger

from pydantic import BaseModel, field_validator

from app.models.db_models import Results, CommandHistory

api_logger = getLogger('api')


class RobotStateResponse(BaseModel):
    x: int
    y: int
    direction: str
    result: str = Results.OK


class RobotStateFailedResponse(BaseModel):
    result: str = Results.OK


class CommandRequest(BaseModel):
    commands: str

    @field_validator('commands')
    def commands_must_be_valid(cls, commands: str) -> str:
        CommandHistory.is_valid_command(commands)
        return commands
