from dataclasses import dataclass
from pathlib import Path

from src.domain.common.exceptions import AppError


@dataclass
class Config:
    storage_path: Path
    page_size: int | None


class ConfigFormatError(AppError):
    @property
    def title(self) -> str:
        return "Invalid format of config"


@dataclass(eq=False)
class ConfigMissingField(AppError):
    field: str

    @property
    def title(self) -> str:
        return f"Config missing required field: {self.field!r}"
