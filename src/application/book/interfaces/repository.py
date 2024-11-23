from abc import abstractmethod
from typing import Protocol

from src.application.book import dto
from src.application.common.pagination import Pagination
from src.domain.book.entity import Book


class BookRepository(Protocol):
    @abstractmethod
    def save_book(self, book: dto.NewBook) -> int:
        """
        Save book to storage.
        Duplicates of books will raise error.

        :param book: Object of new book
        :return: ID of saved book
        :raise BookAlreadyExists: If book with same data already exists:
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
        Count books by filters. Filters field will union (logical AND).
        :return: Count of accepted books.
        """
        raise NotImplementedError

    @abstractmethod
    def update_book(self, book: Book):
        """
        Full updates book in storage.
        :param book: Updated book object
        :raise BookNotFound: If book with given ID not exists
        :raise BookAlreadyExists: If book with same data, but different ID already exists.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_book(self, book_id: int):
        """
        Delete book from storage by ID
        :raise BookNotFound: If book with given ID not exists
        """

        raise NotImplementedError

    @abstractmethod
    def get_book_by_id(self, book_id: int) -> Book:
        """
        Get book by ID
        :raise BookNotFound: If book with given ID not exists
        """
        raise NotImplementedError
