import json
import typing
from json import JSONDecodeError
from pathlib import Path

from src.infrastructure.db.json import IOProvider


class FileJsonProvider(IOProvider):
    def __init__(self, path: str | Path):
        self._path = Path(path)

    def read_json(self) -> typing.Any:
        if not self._path.exists():
            return None

        with open(self._path, mode="r+", encoding="utf-8") as f:
            try:
                return json.load(f)
            except JSONDecodeError as err:
                if err.pos == 0:
                    # File is empty it means None schema
                    # This case handled in Schema.from_json
                    return None

                raise err

    def write_json(self, data: typing.Any) -> None:
        with self._path.open(mode="w+", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
