from logging import getLogger

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config.exception_handlers import InvalidData
from app.config.settings import SETTINGS
from app.models.db_models import RobotState

api_logger = getLogger('api')


def get_or_create_robot_state(db: Session) -> RobotState:
    try:
        state = db.query(RobotState).first()
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
