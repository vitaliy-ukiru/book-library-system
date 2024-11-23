from src.application.book import dto
from src.application.book.interfaces import BookRepository
from src.application.common.pagination import Pagination, PaginationResult
from src.domain.book.entity import Book
from src.domain.book.vo import BookStatus


class Service:
    _repo: BookRepository

    def __init__(self, _repo: BookRepository):
        self._repo = _repo

    def create_book(self, book: dto.CreateBook) -> Book:
        new_book = dto.NewBook(
            title=book.title.strip(),
            author=book.author.strip(),
            year=book.year,
            status=BookStatus.AVAILABLE,
        )

        book_id = self._repo.save_book(new_book)

        return Book(
            id=book_id,
            title=new_book.title,
            author=new_book.author,
            year=new_book.year,
            status=new_book.status,
        )

    def delete_book(self, book_id: int):
        self._repo.delete_book(book_id)

    def update_status(self, book_id: int, status: BookStatus):
        book = self._repo.get_book_by_id(book_id)
        match status:
            case BookStatus.AVAILABLE:
                book.return_to_library()
            case BookStatus.TAKEN:
                book.take_from_library()

        self._repo.update_book(book)

    def find_books(self, filters: dto.BookFilter, pagination: Pagination) -> dto.Books:
        books = self._repo.find_books(filters, pagination)
        total_count = self._repo.get_book_count(filters)

        return dto.Books(
            data=books,
            pagination=PaginationResult.from_pagination(pagination, total_count)
        )

