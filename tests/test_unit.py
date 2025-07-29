import pytest

from app.models.db_models import RobotState, Directions
from app.service import get_or_create_robot_state, check_obstacle, move_robot


class DummySettings:
    start_x = 0
    start_y = 0
    start_direction = Directions.NORTH
    obstacles = {(1, 1)}


@pytest.fixture(autouse=True)
def patch_settings(monkeypatch):
    import app.service
    monkeypatch.setattr(app.service, 'SETTINGS', DummySettings)


@pytest.fixture
def dummy_db():
    class DummyQuery:
        def order_by(self, *args, **kwargs):
            return self

        def first(self):
            return None

    class DummySession:
        def query(self, *args, **kwargs):
            return DummyQuery()

        def add(self, obj):
            pass

        def commit(self):
            pass

        def refresh(self, obj):
            pass

    return DummySession()


def test_get_or_create_robot_state_creates_new(dummy_db):
    state = get_or_create_robot_state(dummy_db)
    assert state.x == 0
    assert state.y == 0
    assert state.direction == Directions.NORTH


def test_check_obstacle_true():
    state = RobotState(x=1, y=1, direction=Directions.NORTH)
    assert check_obstacle(state) is True


def test_check_obstacle_false():
    state = RobotState(x=0, y=0, direction=Directions.NORTH)
    assert check_obstacle(state) is False


def test_move_robot_forward():
    state = RobotState(x=0, y=0, direction=Directions.NORTH)
    new_state, obstacle = move_robot(state, 'F')
    assert (new_state.x, new_state.y) == (0, 1)
    assert not obstacle


def test_move_robot_left():
    state = RobotState(x=0, y=0, direction=Directions.NORTH)
    new_state, _ = move_robot(state, 'L')
    assert new_state.direction == Directions.WEST


def test_move_robot_right():
    state = RobotState(x=0, y=0, direction=Directions.NORTH)
    new_state, _ = move_robot(state, 'R')
    assert new_state.direction == Directions.EAST


def test_move_robot_backward():
    state = RobotState(x=0, y=0, direction=Directions.NORTH)
    new_state, _ = move_robot(state, 'B')
    assert (new_state.x, new_state.y) == (0, -1)


def test_move_robot_hits_obstacle():
    state = RobotState(x=0, y=0, direction=Directions.EAST)
    # Move to (1,0), then (1,1) which is an obstacle
    state, _ = move_robot(state, 'F')
    state, _ = move_robot(state, 'L')
    state, obstacle = move_robot(state, 'F')

    assert (state.x, state.y) == (1, 1)
    assert obstacle


def test_move_robot_invalid_command():
    state = RobotState(x=0, y=0, direction=Directions.NORTH)
    # Should not change state for invalid command
    orig = (state.x, state.y, state.direction)
    new_state, obstacle = move_robot(state, 'X')
    assert (new_state.x, new_state.y, new_state.direction) == orig
    assert not obstacle


def test_move_robot_multiple_commands():
    state = RobotState(x=0, y=0, direction=Directions.NORTH)
    cmds = ['F', 'R', 'F', 'L', 'B']
    for cmd in cmds:
        state, _ = move_robot(state, cmd)
    # Final position should be (1, 0) facing NORTH
    assert (state.x, state.y) == (1, 0)
    assert state.direction == Directions.NORTH


def test_get_or_create_robot_state_existing(monkeypatch):
    class DummyState:
        x, y, direction = 5, 5, Directions.SOUTH
    class DummyQuery:
        def order_by(self, *args, **kwargs):
            return self
        def first(self):
            return DummyState()
    class DummySession:
        def query(self, *args, **kwargs):
            return DummyQuery()
    state = get_or_create_robot_state(DummySession())
    assert state.x == 5 and state.y == 5 and state.direction == Directions.SOUTH


def test_check_obstacle_negative():
    state = RobotState(x=-1, y=-1, direction=Directions.NORTH)
    assert not check_obstacle(state)
