from configparser import ConfigParser
from pathlib import Path

from src.config.config import Config, ConfigFormatError, ConfigMissingField


def load_config(path: str) -> Config:
    parser = ConfigParser()

    parser.read(path)
    if not parser.has_section("main"):
        raise ConfigFormatError()

    main = parser["main"]

    storage_path = main.get("storage.path")
    if not storage_path:
        raise ConfigMissingField("storage.path")

    page_size = main.getint("page_size")
    if page_size == 0:
        page_size = 10

    return Config(
        storage_path=Path(storage_path),
        page_size=page_size,
    )
