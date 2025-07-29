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
    command: str

    @field_validator('command')
    def command_must_be_valid(cls, command: str) -> str:
        CommandHistory.is_valid_command(command)
        return command
