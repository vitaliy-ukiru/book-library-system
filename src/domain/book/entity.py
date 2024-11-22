from dataclasses import dataclass

from src.domain.book.exceptions import BookAlreadyTaken, BookAlreadyInLibrary
from src.domain.book.vo import BookStatus


@dataclass
class Book:
    id: int
    title: str
    author: str
    year: int
    status: BookStatus

    def take_from_library(self):
        """
        Take book from library storage.
        Raises BookAlreadyTaken if book is already in-hands.
        """
        if self.status is BookStatus.TAKEN:
            raise BookAlreadyTaken(self.id)

        self.status = BookStatus.TAKEN

    def return_to_library(self):
        """
        Return book to library storage.
        Raises BookAlreadyInLibrary if book is already in library.
        """

        if self.status is BookStatus.AVAILABLE:
            raise BookAlreadyInLibrary(self.id)

        self.status = BookStatus.AVAILABLE
