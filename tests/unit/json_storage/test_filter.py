import pytest

from src.application.book.dto import BookFilter
from src.infrastructure.db.json.filter import FilterFactory
from src.infrastructure.db.json.schema import BookSchema


@pytest.fixture
def good_book():
    return BookSchema(
        id=1,
        title="Awesome book",
        author="Bob Robinson",
        year=1970,
        status=True
    )

@pytest.fixture
def bad_book():
    return BookSchema(
        id=2,
        title="Bad book",
        author="John Taylor",
        year=1971,
        status=True
    )

def test_title(good_book, bad_book):
    f = FilterFactory.title("awesome")
    assert f(good_book)
    assert not f(bad_book)


def test_author(good_book, bad_book):
    f = FilterFactory.author("bob")
    assert f(good_book)
    assert not f(bad_book)


def test_year(good_book, bad_book):
    f = FilterFactory.year(1970)
    assert f(good_book)
    assert not f(bad_book)


def test_and_(good_book, bad_book):
    f = FilterFactory.and_((
        FilterFactory.title("awesome"),
        FilterFactory.author("bob"),
    ))

    assert f(good_book)
    assert not f(bad_book)


def test_from_dto(good_book):
    good_filter = FilterFactory.from_dto(BookFilter(
        title="awesome book",
        author="bob"
    ))

    bad_filter = FilterFactory.from_dto(BookFilter(
        title="awesome book",
        author="bob",
        year=2000,
    ))

    assert good_filter(good_book)
    assert not bad_filter(good_book)
