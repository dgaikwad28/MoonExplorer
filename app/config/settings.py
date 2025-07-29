import os

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class Settings(BaseSettings):
    debug: bool = False
    secret_key: str
    environment: str
    app_name: str = "Moon Explorer"

    allowed_hosts: list
    https_only: bool = True

    # database credential
    db_url: str
    db_multi_thread: bool = False

    # initial robot state
    start_x: int = 4
    start_y: int = 2
    start_direction: str = "west"

    obstacles: set[tuple[int, int]] = {(1, 4), (3, 5), (7, 4)}

    model_config = SettingsConfigDict(env_file=os.path.join(ROOT_DIR, "env", ".env"), extra='ignore')


SETTINGS = Settings()

# @lru_cache()
# def get_settings():
#     return Settings()
