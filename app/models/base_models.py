from pydantic import BaseModel


class RobotStateResponse(BaseModel):
    x: int
    y: int
    direction: str


class CommandRequest(BaseModel):
    commands: str
