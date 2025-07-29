from copy import deepcopy
from logging import getLogger

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config.session import get_db
from app.models.base_models import RobotStateResponse, CommandRequest, RobotStateFailedResponse
from app.models.db_models import CommandHistory, RobotState, Results
from app.service import get_or_create_robot_state, move_robot

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


@api_router.post("/commands", response_model=RobotStateResponse)
def execute_commands(req: CommandRequest, db: Session = Depends(get_db)):
    try:
        present_state = get_or_create_robot_state(db)
        # Create a copy of the state to avoid mutating the original
        present_state_copy = deepcopy(present_state)
        # Store the command as a single entry in CommandHistory
        command_history = CommandHistory(command=req.commands)
        db.add(command_history)
        db.flush()  # To get command_history.id

        new_state_obj = None
        # Process commands and update state, saving each state after a command
        for cmd in req.commands:
            updated_present_state, error_occurred = move_robot(present_state_copy, cmd)
            if error_occurred:
                command_history.result = Results.OBSTACLE
                db.commit()
                return RobotStateResponse(x=present_state_copy.x, y=present_state_copy.y,
                                          direction=present_state_copy.direction)
            new_state_obj = RobotState(
                x=updated_present_state.x,
                y=updated_present_state.y,
                direction=updated_present_state.direction,
                command_id=command_history.id
            )
            db.add(new_state_obj)

        # Mark command_history as executed after successful commit
        command_history.executed = True
        command_history.result = Results.OK
        db.commit()

        if new_state_obj:
            db.refresh(new_state_obj)
            return RobotStateResponse(x=new_state_obj.x, y=new_state_obj.y, direction=new_state_obj.direction,
                                      result=Results.OK)
    except Exception as exc:
        api_logger.exception(f'Error executing commands: {exc}')
        db.rollback()

    finally:
        db.close()
        api_logger.debug('Database session closed.')

    return RobotStateFailedResponse(result=Results.FAILED)
