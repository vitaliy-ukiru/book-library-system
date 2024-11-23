import typing

from src.infrastructure.db.json import IOProvider


class MockIOProvider(IOProvider):
    def __init__(self, data: typing.Any):
        self.data = data

    def __repr__(self):
        return f'MockIOProvider(data={self.data!r})'

    def read_json(self) -> typing.Any:
        return self.data

    def write_json(self, data: typing.Any):
        self.data = data
