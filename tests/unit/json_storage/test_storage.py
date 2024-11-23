import pytest

from src.application.book.dto import BookFilter
from src.application.common.pagination import Pagination
from src.infrastructure.db.json import JsonStorage
from src.infrastructure.db.json.schema import _SchemaJson, _BookJson
from tests.mocks.json_io_provider import MockIOProvider


@pytest.fixture
def schema_json():
    return _SchemaJson(
        last_id=10,
        books=[
            _BookJson(
                id=i,
                title=f"book-{i}",
                author="foo" if i % 2 == 0 else "bar" if i % 3 == 0 else "baz",
                year=0,
                status=True,
            )

            for i in range(1, 11)
        ]
    )


@pytest.fixture
def storage(schema_json):
    return JsonStorage(MockIOProvider(schema_json))


def test_storage_search(storage):
    f = BookFilter(author="foo")
    books = storage.find_books(filters=f, pagination=Pagination(
        offset=2, limit=10
    ))

    assert [book.id for book in books] == [6, 8, 10]
    assert storage.get_book_count(f) == 5

    assert len(storage.find_books(BookFilter(), Pagination())) == 10
