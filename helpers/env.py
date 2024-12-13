from importlib.resources import path
import pathlib
from functools import lru_cache

from decouple import Config, RepositoryEnv

THIS_DIR = pathlib.Path(__file__).resolve().parent
BASE_DIR = THIS_DIR.parent
BASE_DIR_ENV = BASE_DIR / ".env"


@lru_cache
def get_config():
    if BASE_DIR_ENV.exists():
        return Config(RepositoryEnv(str(BASE_DIR_ENV)))
    from decouple import config

    return config


config = get_config()
