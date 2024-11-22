from abc import abstractmethod
from typing import Protocol, Iterable

from src.application.book.dto import BookFilter
from src.infrastructure.db.json.schema import BookSchema


class Filter(Protocol):
    """
    Filter for linear search of books by collection.


    Filters must be just callable object that returns bool.
    """
    @abstractmethod
    def __call__(self, book: BookSchema) -> bool:
        raise NotImplementedError


class FilterFactory:
    """
    FilterFactory just contains required filters for JsonStorage.
    """

    @staticmethod
    def title(title: str) -> Filter:
        return lambda book: title in book.title

    @staticmethod
    def author(author: str) -> Filter:
        return lambda book: author in book.author

    @staticmethod
    def year(year: int) -> Filter:
        return lambda book: year == book.year

    @staticmethod
    def and_(filters: Iterable[Filter]) -> Filter:
        return lambda book: all(f(book) for f in filters)

    @classmethod
    def _yield_filters(cls, filters: BookFilter) -> Iterable[Filter]:
        if filters.title:
            yield cls.title(filters.title)

        if filters.author:
            yield cls.author(filters.author)

        if filters.year:
            yield cls.year(filters.year)

    @classmethod
    def from_dto(cls, filters: BookFilter) -> Filter:
        return cls.and_(tuple(cls._yield_filters(filters)))