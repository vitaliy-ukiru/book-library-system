from dataclasses import dataclass

from src.application.common.dto import DTO
from src.domain.book.vo import BookStatus


@dataclass(frozen=True)
class CreateBook(DTO):
    title: str
    author: str
    year: int


@dataclass(frozen=True)
class NewBook(CreateBook):
    status: BookStatus

    @classmethod
    def from_create_book_dto(cls, book: CreateBook, status: BookStatus):
        return cls(
            title=book.title,
            author=book.author,
            year=book.year,
            status=status,
        )


@dataclass(frozen=True)
class BookFilter(DTO):
    title: str | None = None
    author: str | None = None
    year: int | None = None


