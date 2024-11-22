from dataclasses import dataclass

from src.application.common.exceptions import ApplicationError
from src.domain.common.exceptions import DomainError


@dataclass(eq=False)
class BookAlreadyExists(ApplicationError):
    book_id: int

    @property
    def title(self) -> str:
        return f'The book already exists with "{self.book_id}" id'


@dataclass(eq=False)
class BookNotFound(DomainError):
    @property
    def title(self) -> str:
        return "A book not found"
