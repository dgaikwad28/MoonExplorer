import pytest
from app.models.db_models import RobotState, Directions, CommandHistory
from app.service import get_or_create_robot_state, check_obstacle, move_robot
from app.config.exception_handlers import InvalidData, IncorrectConfiguration


class TestRobotStateDB:
    def test_get_or_create_robot_state_creates_new(self, dummy_db):
        state = get_or_create_robot_state(dummy_db)
        assert state.x == 0
        assert state.y == 0
        assert state.direction == Directions.NORTH

    def test_get_or_create_robot_state_existing(self, monkeypatch):
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


class TestObstacle:
    def test_check_obstacle_true(self):
        state = RobotState(x=1, y=1, direction=Directions.NORTH)
        assert check_obstacle(state) is True

    def test_check_obstacle_false(self):
        state = RobotState(x=0, y=0, direction=Directions.NORTH)
        assert check_obstacle(state) is False

    def test_check_obstacle_negative(self):
        state = RobotState(x=-1, y=-1, direction=Directions.NORTH)
        assert not check_obstacle(state)


class TestMoveRobot:
    def test_move_robot_forward(self):
        state = RobotState(x=0, y=0, direction=Directions.NORTH)
        new_state, obstacle = move_robot(state, 'F')
        assert (new_state.x, new_state.y) == (0, 1)
        assert not obstacle

    def test_move_robot_left(self):
        state = RobotState(x=0, y=0, direction=Directions.NORTH)
        new_state, _ = move_robot(state, 'L')
        assert new_state.direction == Directions.WEST

    def test_move_robot_right(self):
        state = RobotState(x=0, y=0, direction=Directions.NORTH)
        new_state, _ = move_robot(state, 'R')
        assert new_state.direction == Directions.EAST

    def test_move_robot_backward(self):
        state = RobotState(x=0, y=0, direction=Directions.NORTH)
        new_state, _ = move_robot(state, 'B')
        assert (new_state.x, new_state.y) == (0, -1)

    def test_move_robot_hits_obstacle(self):
        state = RobotState(x=0, y=0, direction=Directions.EAST)
        # Move to (1,0), then (1,1) which is an obstacle
        state, _ = move_robot(state, 'F')
        state, _ = move_robot(state, 'L')
        state, obstacle = move_robot(state, 'F')

        assert (state.x, state.y) == (1, 1)
        assert obstacle

    def test_move_robot_invalid_command(self):
        state = RobotState(x=0, y=0, direction=Directions.NORTH)
        # Should not change state for invalid command
        orig = (state.x, state.y, state.direction)
        new_state, obstacle = move_robot(state, 'X')
        assert (new_state.x, new_state.y, new_state.direction) == orig
        assert not obstacle

    def test_move_robot_multiple_commands(self):
        state = RobotState(x=0, y=0, direction=Directions.NORTH)
        cmds = ['F', 'R', 'F', 'L', 'B']
        for cmd in cmds:
            state, _ = move_robot(state, cmd)
        # Final position should be (1, 0) facing NORTH
        assert (state.x, state.y) == (1, 0)
        assert state.direction == Directions.NORTH


class TestStaticMethods:
    def test_is_valid_direction_valid(self):
        assert RobotState.is_valid_direction('north')
        assert RobotState.is_valid_direction('south')
        assert RobotState.is_valid_direction('east')
        assert RobotState.is_valid_direction('west')

    def test_is_valid_direction_invalid(self):
        assert not RobotState.is_valid_direction('northeast')
        assert not RobotState.is_valid_direction('')
        assert not RobotState.is_valid_direction(None)

    def test_is_valid_result_valid(self):
        assert CommandHistory.is_valid_result('ok')
        assert CommandHistory.is_valid_result('failed')
        assert CommandHistory.is_valid_result('obstacle')

    def test_is_valid_result_invalid(self):
        assert not CommandHistory.is_valid_result('success')
        assert not CommandHistory.is_valid_result('')
        assert not CommandHistory.is_valid_result(None)

    def test_is_valid_command_valid(self):
        assert CommandHistory.is_valid_command('F')
        assert CommandHistory.is_valid_command('LRFB')
        assert CommandHistory.is_valid_command('')  # Empty string is technically valid (no invalid chars)

    def test_is_valid_command_invalid(self):
        with pytest.raises(IncorrectConfiguration):
            CommandHistory.is_valid_command('X')
        with pytest.raises(IncorrectConfiguration):
            CommandHistory.is_valid_command('FZ')
        with pytest.raises(IncorrectConfiguration):
            CommandHistory.is_valid_command('123')
        with pytest.raises(IncorrectConfiguration):
            CommandHistory.is_valid_command('f')  # Lowercase is not valid
