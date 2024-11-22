from abc import abstractmethod
from typing import Protocol

from src.application.book import dto
from src.application.common.pagination import Pagination
from src.domain.book.entity import Book


class BookRepository(Protocol):
    @abstractmethod
    def save_book(self, book: dto.NewBook) -> int:
        """
        Saves book to storage
        :param book: Book object
        :return: Saved book id
        """
        raise NotImplementedError

    @abstractmethod
    def find_books(self, filters: dto.BookFilter, pagination: Pagination) -> list[Book]:
        """
        Finds books based on filters and paginate result
        """
        raise NotImplementedError

    @abstractmethod
    def get_book_count(self, filters: dto.BookFilter) -> int:
        """
        Counts books accepted to filter
        """
        raise NotImplementedError

    @abstractmethod
    def update_book(self, book: Book):
        raise NotImplementedError

    @abstractmethod
    def delete_book(self, book_id: int):
        raise NotImplementedError

    @abstractmethod
    def get_book_by_id(self, book_id: int) -> Book:
        raise NotImplementedError
