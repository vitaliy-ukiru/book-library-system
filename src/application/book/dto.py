from dataclasses import dataclass
from typing import TypeAlias

from src.application.common.dto import DTO
from src.application.common.pagination import PaginatedItemsDTO
from src.domain.book import entity
from src.domain.book.vo import BookStatus


@dataclass(frozen=True)
class CreateBook(DTO):
    title: str
    author: str
    year: int


@dataclass(frozen=True)
class NewBook(CreateBook):
    status: BookStatus


@dataclass(frozen=True)
class BookFilter(DTO):
    title: str | None = None
    author: str | None = None
    year: int | None = None

    @property
    def is_empty(self) -> bool:
        return (self.title is None and
                self.author is None and
                self.year is None)


Books: TypeAlias = PaginatedItemsDTO[entity.Book]
