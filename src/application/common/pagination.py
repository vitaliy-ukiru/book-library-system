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


@dataclass(frozen=True)
class PaginatedItemsDTO(DTO, Generic[Item]):
    data: list[Item]
    pagination: PaginationResult

