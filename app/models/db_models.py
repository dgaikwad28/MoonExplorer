from logging import getLogger

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship

from app.config.exception_handlers import InvalidData
from app.config.session import Base

api_logger = getLogger('api')


class Directions:
    NORTH = 'north'
    SOUTH = 'south'
    EAST = 'east'
    WEST = 'west'

    ALL = {NORTH, SOUTH, EAST, WEST}

    # IMPORTANT: Don't change the order.
    direction_order = [NORTH, EAST, SOUTH, WEST]


class Results:
    OK = 'ok'
    FAILED = 'failed'
    OBSTACLE = 'obstacle'

    ALL = {OK, FAILED, OBSTACLE}


class RobotState(Base):
    __tablename__ = "robot_state"

    id = Column(Integer, primary_key=True)

    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    direction = Column(String, nullable=False)

    timestamp = Column(DateTime, default=func.now(), nullable=False, index=True)
    command_id = Column(Integer, ForeignKey('command_history.id', ondelete='SET NULL'), nullable=True)
    command = relationship("CommandHistory", back_populates="robot_states", passive_deletes=True)

    @staticmethod
    def is_valid_direction(direction):
        return direction in Directions.ALL


class CommandHistory(Base):
    __tablename__ = "command_history"

    id = Column(Integer, primary_key=True)

    command = Column(String, nullable=False)
    executed = Column(Boolean, default=False)
    result = Column(String, nullable=True)

    timestamp = Column(DateTime, default=func.now(), nullable=False)
    robot_states = relationship("RobotState", back_populates="command", lazy="dynamic")

    @staticmethod
    def is_valid_result(result):
        return result in Results.ALL

    @staticmethod
    def is_valid_command(command: str) -> bool:
        if not all(c in 'FBLR' for c in command):
            api_logger.info(f'Invalid command: {command}')
            raise InvalidData()
        return True
