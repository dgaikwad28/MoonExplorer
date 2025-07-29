from logging import getLogger

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config.session import get_db
from app.models.base_models import RobotStateResponse, CommandRequest
from app.service import get_or_create_robot_state

api_router = APIRouter(prefix="/api", tags=["api"])
api_logger = getLogger('api')


@api_router.get(
    "/state",
    summary="Get the current state of the robot",
    status_code=status.HTTP_200_OK,
    response_model=RobotStateResponse
)
def get_state(db: Session = Depends(get_db)) -> RobotStateResponse:
    state = get_or_create_robot_state(db)
    return RobotStateResponse(x=state.x, y=state.y, direction=state.direction)
