import pytest

from src.application.book.exceptions import BookAlreadyExists, BookNotFound
from src.infrastructure.db.json.schema import Schema, BookSchema


def test_book_schema_hash():
    a = BookSchema(
        id=1,
        title="A",
        author="B",
        year=1,
        status=True,
    )

    a_copy = BookSchema(
        id=2,
        title="a",
        author="b",
        year=1,
        status=False,
    )

    assert a.hash == a_copy.hash

    b = BookSchema(
        id=0,
        title="b",
        author="a",
        year=1,
        status=True
    )

    assert a.hash != b.hash


def test_insert():
    schema = Schema()

    schema.insert(BookSchema(
        id=schema.next_id(),
        title="test",
        author="tester",
        year=1,
        status=False
    ))

    with pytest.raises(BookAlreadyExists):
        schema.insert(BookSchema(
            id=schema.next_id(),
            title="Test",
            author="tEster",
            year=1,
            status=True,
        ))


def test_update():
    schema = Schema(
        last_id=2,
        books={
            1: BookSchema(
                id=1,
                title="test",
                author="tester",
                year=1,
                status=True,
            ),
            2: BookSchema(id=2, title="Foo", author="Bar", year=1, status=False)

        }
    )

    # Case 1: Successfully update
    schema.update(BookSchema(
        id=1,
        title="test",
        author="tester",
        year=1,
        status=False,
    ))

    assert not schema.books[1].status  # ensure update

    # Case 2: Not book with id
    with pytest.raises(BookNotFound):
        schema.update(BookSchema(id=3, title="", author="", year=0, status=False))

        # Case 3: Book duplicate
    with pytest.raises(BookAlreadyExists):
        schema.update(BookSchema(
            id=2,
            title="Test",
            author="Tester",
            year=1,
            status=True,
        ))


def test_delete():
    schema = Schema(
        last_id=2,
        books={
            1: BookSchema(
                id=1,
                title="test",
                author="tester",
                year=1,
                status=True,
            ),

        }
    )

    schema.delete(book_id=1)
    assert len(schema.books) == 0
    assert len(schema._hashes) == 0

    with pytest.raises(BookNotFound):
        schema.delete(book_id=1)


