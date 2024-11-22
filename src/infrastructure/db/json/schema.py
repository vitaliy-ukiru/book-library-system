import hashlib
import typing
from dataclasses import dataclass, field
from typing import TypedDict

from src.application.book.exceptions import BookAlreadyExists, BookNotFound
from src.application.common.exceptions import MappingError
from src.domain.book.entity import Book
from src.domain.book.vo import BookStatus


class _BookJson(TypedDict):
    """
    _BookJson is representation how book object will in JSON.
    """
    id: int
    title: str
    author: str
    year: int
    status: bool


class _SchemaJson(TypedDict):
    """
    _SchemaJson is representation how global schema object will in JSON.
    """
    last_id: int
    books: list[_BookJson]


@dataclass
class BookSchema:
    """
    BookSchema is runtime representation of book from JSON storage.
    """
    id: int
    title: str
    author: str
    year: int

    status: bool  # Status reports is book available for take.

    def _status_convert(self) -> BookStatus:
        return BookStatus.AVAILABLE if self.status else BookStatus.TAKEN

    def to_entity(self) -> Book:
        return Book(
            id=self.id,
            title=self.title,
            author=self.author,
            year=self.year,
            status=self._status_convert(),
        )

    def to_json(self) -> _BookJson:
        return _BookJson(
            id=self.id,
            title=self.title,
            author=self.author,
            year=self.year,
            status=self.status,
        )

    @property
    def hash(self):
        """
        Calculates hash for book. It needs to exclude same books (Title+Author+Year)
        """
        h = hashlib.sha1(usedforsecurity=False)
        h.update(self.title.lower().encode())
        h.update(self.author.lower().encode())
        h.update(str(self.year).encode())
        return h.hexdigest()


@dataclass
class Schema:
    """
    Schema is runtime representation of schema from JSON storage.

    Books are stored as dict where key is book id for fast search by ID.

    Hashes also stored like dict (hash -> book_id). For fast create/delete/update operations.
    """

    last_id: int = field(default=0)  # Like auto-increment

    books: dict[int, BookSchema] = field(default_factory=dict)

    _hashes: dict[str, int] = field(init=False)

    def __post_init__(self):
        self._hashes = {
            book.hash: book.id

            for book in self.books.values()
        }

    def next_id(self) -> int:
        self.last_id += 1
        return self.last_id

    def insert(self, book: BookSchema):

        book_hash = book.hash
        existing_book = self._hashes.get(book_hash)
        if existing_book:
            raise BookAlreadyExists(existing_book)

        self.books[book.id] = book
        self._hashes[book_hash] = book.id

    def update(self, book: BookSchema):
        # Lookup book from schema
        book_prev = self.books.get(book.id)
        if not book_prev:
            raise BookNotFound()

        # Lookup book with same hash
        existing_book_id = self._hashes.get(book.hash)
        if existing_book_id and existing_book_id != book_prev.id:
            # Book with same hash can already exist but with different id
            raise BookAlreadyExists(existing_book_id)

        self.books[book.id] = book

        del self._hashes[book_prev.hash]
        self._hashes[book.hash] = book.id

    def delete(self, book_id: int):
        book = self.books.pop(book_id, None)
        if book is None:
            raise BookNotFound()

        del self._hashes[book.hash]

    def to_json(self) -> _SchemaJson:
        return _SchemaJson(
            last_id=self.last_id,
            books=[
                book.to_json()
                for book in self.books.values()
            ]
        )

    @classmethod
    def from_json(cls, data: typing.Any):
        if data is None:
            # Common case for empty file
            return cls()

        if not isinstance(data, dict):
            raise MappingError("Invalid root schema format")

        last_id = data.get("last_id")
        if last_id is None:
            raise MappingError("The field `last_id` is missing")

        if not isinstance(last_id, int):
            raise MappingError("The field `last_id` must be an integer")

        books_raw: list[typing.Any] = data.get("books", [])
        if not isinstance(books_raw, list):
            raise MappingError("The field `books` must be a list")

        books = {}
        for i, book_raw in enumerate(books_raw):

            if not isinstance(book_raw, dict):
                raise MappingError(f"The object `book` must be a dictionary for book with index {i}")
            try:
                book = BookSchema(
                    id=int(book_raw["id"]),
                    title=str(book_raw["title"]),
                    author=str(book_raw["author"]),
                    year=int(book_raw["year"]),
                    status=bool(book_raw["status"]),
                )
            except KeyError as err:
                key = err.args[0]
                raise MappingError(f"Missing field {key!r} for book with index {i}")

            books[book.id] = book

        return cls(last_id=last_id, books=books)
