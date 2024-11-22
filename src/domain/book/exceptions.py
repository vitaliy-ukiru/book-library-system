from dataclasses import dataclass

from src.domain.common.exceptions import DomainError


@dataclass(eq=False)
class BookAlreadyTaken(DomainError):
    id: int

    @property
    def title(self) -> str:
        return f"The book with {self.id} id already taken"


@dataclass(eq=False)
class BookAlreadyInLibrary(DomainError):
    id: int

    @property
    def title(self) -> str:
        return f"The book with {self.id} id already in library"

