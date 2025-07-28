import os
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/moonrobot")
START_X = int(os.getenv("START_X", 4))
START_Y = int(os.getenv("START_Y", 2))
START_DIRECTION = os.getenv("START_DIRECTION", "WEST")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


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
    timestamp = Column(DateTime, default=datetime.utcnow)
    result = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


class RobotStateResponse(BaseModel):
    x: int
    y: int
    direction: str


class CommandRequest(BaseModel):
    commands: str


# Initialize robot state if not present
def get_or_create_robot_state(db):
    state = db.query(RobotState).first()
    if not state:
        state = RobotState(x=START_X, y=START_Y, direction=START_DIRECTION)
        db.add(state)
        db.commit()
        db.refresh(state)
    return state


DIRECTIONS = ["NORTH", "EAST", "SOUTH", "WEST"]
MOVE_MAP = {
    "NORTH": (0, 1),
    "EAST": (1, 0),
    "SOUTH": (0, -1),
    "WEST": (-1, 0)
}


def move_robot(state, command):
    dx, dy = MOVE_MAP[state.direction]
    if command == "F":
        state.x += dx
        state.y += dy
    elif command == "B":
        state.x -= dx
        state.y -= dy
    # else: ignore invalid commands
    return state


@app.get("/state", response_model=RobotStateResponse)
def get_state():
    db = SessionLocal()
    try:
        state = get_or_create_robot_state(db)
        return RobotStateResponse(x=state.x, y=state.y, direction=state.direction)
    finally:
        db.close()


@app.post("/commands", response_model=RobotStateResponse)
def execute_commands(req: CommandRequest):
    db = SessionLocal()
    try:
        state = get_or_create_robot_state(db)
        result = []
        for cmd in req.commands:
            if cmd in ("F", "B"):
                move_robot(state, cmd)
                db.add(CommandHistory(command=cmd, result=f"({state.x},{state.y}) {state.direction}"))
        db.commit()
        db.refresh(state)
        return RobotStateResponse(x=state.x, y=state.y, direction=state.direction)
    finally:
        db.close()
