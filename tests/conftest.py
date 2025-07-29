import pytest

from app.models.db_models import Directions


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


class DummySettings:
    start_x = 0
    start_y = 0
    start_direction = Directions.NORTH
    obstacles = {(1, 1)}
