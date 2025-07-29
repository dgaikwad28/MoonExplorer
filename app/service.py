from logging import getLogger

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config.exception_handlers import InvalidData
from app.config.settings import SETTINGS
from app.models.db_models import RobotState, Directions

api_logger = getLogger('api')


def get_or_create_robot_state(db: Session) -> RobotState:
    """
    Retrieve the latest robot state from the database, or create a new one with initial settings if none exists.
    """
    try:
        state = db.query(RobotState).order_by(RobotState.timestamp.desc(), RobotState.id.desc()).first()
        if not state:
            api_logger.debug('No robot state found, creating a new one with initial settings.')
            state = RobotState(x=SETTINGS.start_x, y=SETTINGS.start_y, direction=SETTINGS.start_direction)
            db.add(state)
            db.commit()
            db.refresh(state)
        return state
    except IntegrityError:
        api_logger.exception('Integrity error when adding new robot state')
        raise InvalidData()
    except Exception as exc:
        api_logger.exception(f'Unexpected error: {exc}')
        raise InvalidData()


def check_obstacle(state: RobotState) -> bool:
    """
    Check if the given coordinates (x, y) are within the bounds of the robot's movement area.
    Returns True if there is an obstacle , False otherwise.
    """
    if (state.x, state.y) in SETTINGS.obstacles:
        api_logger.debug(f'Obstacle detected at ({state.x}, {state.y})')
        return True
    return False


def move_robot(state: RobotState, cmd: str) -> (RobotState, bool):
    """
    Move or rotate the robot based on its current state and a command.
    command:
        F: Move forward
        B: Move backward
        L: Rotate left
        R: Rotate right
    """
    direction_delta = {Directions.NORTH: (0, 1), Directions.EAST: (1, 0), Directions.SOUTH: (0, -1),
                       Directions.WEST: (-1, 0)}
    if cmd == 'L':
        state.direction = Directions.direction_order[(Directions.direction_order.index(state.direction) - 1) % 4]
    elif cmd == 'R':
        state.direction = Directions.direction_order[(Directions.direction_order.index(state.direction) + 1) % 4]
    elif cmd == 'F':
        dx, dy = direction_delta[state.direction]
        state.x += dx
        state.y += dy
    elif cmd == 'B':
        dx, dy = direction_delta[state.direction]
        state.x -= dx
        state.y -= dy

    error_occurred = check_obstacle(state)
    return state, error_occurred
