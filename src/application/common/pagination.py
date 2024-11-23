from dataclasses import dataclass
from typing import Generic, TypeVar

from src.application.common.dto import DTO

Item = TypeVar("Item")


@dataclass(frozen=True)
class Pagination:
    offset: int | None = None
    limit: int | None = None


@dataclass(frozen=True)
class PaginationResult(DTO):
    offset: int | None
    limit: int | None
    total: int

    @classmethod
    def from_pagination(cls, pagination: Pagination, total: int) -> "PaginationResult":
        return cls(offset=pagination.offset, limit=pagination.limit, total=total)

    @property
    def next_page(self) -> bool:
        offset = self.offset or 0

        if self.limit is None:
            return False

        return offset + self.limit < self.total

    @property
    def prev_page(self) -> bool:
        return self.offset is not None and self.offset > 0

@dataclass(frozen=True)
class PaginatedItemsDTO(DTO, Generic[Item]):
    data: list[Item]
    pagination: PaginationResult
