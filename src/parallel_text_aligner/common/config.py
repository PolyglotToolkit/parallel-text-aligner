from pathlib import Path

from .locations import Locations


class ConfigSingleton:
    ...


_CONFIG = ConfigSingleton()


def get_config():
    return _CONFIG
