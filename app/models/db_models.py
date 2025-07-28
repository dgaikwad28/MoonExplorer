import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app.config.session import Base


class RobotState(Base):
    __tablename__ = "robot_state"
    id = Column(Integer, primary_key=True, index=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    direction = Column(String, nullable=False)


class CommandHistory(Base):
    __tablename__ = "command_history"
    id = Column(Integer, primary_key=True, index=True)
    command = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    result = Column(String, nullable=False)
