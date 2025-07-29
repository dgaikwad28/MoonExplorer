from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship

from app.config.session import Base


class Directions:
    NORTH = 'north'
    SOUTH = 'south'
    EAST = 'east'
    WEST = 'west'
    ALL = {NORTH, SOUTH, EAST, WEST}


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

    timestamp = Column(DateTime, default=func.now(), nullable=False)
    robot_states = relationship("RobotState", back_populates="command", lazy="dynamic")
