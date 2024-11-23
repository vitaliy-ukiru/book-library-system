import threading
import typing
from abc import ABC, abstractmethod

from src.application.book import dto
from src.application.book.exceptions import BookNotFound
from src.application.book.interfaces.repository import BookRepository
from src.application.common.pagination import Pagination
from src.domain.book.entity import Book
from src.domain.book.vo import BookStatus
from .filter import FilterFactory
from .schema import BookSchema, Schema
from .utils import paginate_items


class IOProvider(ABC):
    """
    IOProvider represents interface to read/write storage date to disk.
    This interface need for exclude dependency of JSON library and remove
    responsibility for where to store data.

    Also, it'll help in test.

    """

    @abstractmethod
    def read_json(self) -> typing.Any:
        """
        Reads and deserializes JSON.
        If content is empty must be return None.
        """
        raise NotImplementedError

    @abstractmethod
    def write_json(self, data: typing.Any):
        """
        Serializes data to JSON and save it.
        """
        raise NotImplementedError


class JsonStorage(BookRepository):
    _data: Schema

    def __init__(self, provider: IOProvider):
        self._provider = provider
        self._lock = threading.Lock()
        self._read_data()

    def acquire_new_id(self) -> int:
        with self._lock:
            return self._data.next_id()

    def _read_data(self):
        data = self._provider.read_json()
        self._data = Schema.from_json(data)

    def _save_data(self):
        data = self._data.to_json()
        self._provider.write_json(data)

    def save_book(self, book: dto.NewBook) -> int:
        book_id = self.acquire_new_id()
        book_model = BookSchema(
            id=book_id,
            title=book.title,
            author=book.author,
            year=book.year,
            status=convert_book_status_to_bool(book.status)
        )

        self._data.insert(book_model)
        self._save_data()
        return book_id

    def find_books(self, filters: dto.BookFilter, pagination: Pagination) -> list[Book]:
        books_iter = self._data.books.values()

        if not filters.is_empty:
            books_iter = filter(FilterFactory.from_dto(filters), books_iter)

        # noinspection PyTypeChecker
        books = paginate_items(
            pagination,
            len(self._data.books),
            map(BookSchema.to_entity, books_iter),
        )

        return books

    def get_book_count(self, filters: dto.BookFilter) -> int:
        if filters.is_empty:
            return len(self._data.books)

        filter_func = FilterFactory.from_dto(filters)
        count = 0
        for _ in filter(filter_func, self._data.books.values()):
            count += 1

        return count

    def delete_book(self, book_id: int):
        self._data.delete(book_id)
        self._save_data()

    def update_book(self, book: Book):
        book_obj = BookSchema(
            id=book.id,
            title=book.title,
            author=book.author,
            year=book.year,
            status=convert_book_status_to_bool(book.status),
        )

        self._data.update(book_obj)
        self._save_data()

    def get_book_by_id(self, book_id: int) -> Book:
        book = self._data.books.get(book_id)
        if book is None:
            raise BookNotFound()

        return book.to_entity()


def convert_book_status_to_bool(status: BookStatus) -> bool:
    return status is BookStatus.AVAILABLE
