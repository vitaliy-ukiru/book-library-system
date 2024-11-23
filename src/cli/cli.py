import math
import os
from argparse import Namespace

from src.application.book import dto
from src.application.book.exceptions import BookAlreadyExists, BookNotFound
from src.application.book.service import Service
from src.application.common.pagination import Pagination
from src.config.config import Config
from src.domain.book.entity import Book
from src.domain.book.exceptions import BookAlreadyInLibrary, BookAlreadyTaken
from src.domain.book.vo import BookStatus

COMMAND_ALL = "all"
COMMAND_STATUS = 'status'
COMMAND_SEARCH = 'search'
COMMAND_DELETE = 'delete'
COMMAND_ADD = 'add'


def format_book(book: Book) -> str:
    return (f'Id: {book.id}\n'
            f'Title: {book.title!r}\n'
            f'Author: {book.author!r}\n'
            f'Year: {book.year}\n'
            f'Status: {book.status.title()}')


class CLI:
    def __init__(
        self,
        config: Config,
        service: Service,

    ):
        self.service = service
        self.config = config
        self._handlers = {}
        self._bind_commands()

    def _add_book(self, args: Namespace):
        try:
            book = self.service.create_book(dto.CreateBook(
                title=args.title,
                author=args.author,
                year=args.year,
            ))
        except BookAlreadyExists as e:
            print("[ERROR]: Book with same title, author and year already exists with id", e.book_id)
            return

        print(f"Book created")
        print(format_book(book))

    def _delete_book(self, args: Namespace):
        try:
            self.service.delete_book(args.id)
        except BookNotFound:
            print(f"[ERROR]: Book with id {args.book_id} not found")
        else:
            print("Book deleted")

    def _change_status(self, args: Namespace):
        status = BookStatus.AVAILABLE if args.status else BookStatus.TAKEN
        try:
            self.service.update_status(args.id, status)
        except BookAlreadyInLibrary:
            print("[ERROR]: Book already in library")
        except BookAlreadyTaken:
            print("[ERROR]: Book already taken from library")
        except BookNotFound:
            print("[ERROR]: Book not found")
        else:
            print("Book updated")

    def _search_books_common(self, filters: dto.BookFilter, page: int):
        """
        The 'ALL' command is an alias for the 'SEARCH' command without filters only.
        This function combines their common part
        """
        page_size = self.config.page_size
        if not page_size:
            # output all books without pagination
            books = self.service.find_books(
                filters=filters,
                pagination=Pagination()
            )
            for books in books.data:
                print("---------")
                print(format_book(books))
                print("---------")

            print(f"Total books: {books.pagination.total}")
            if page:
                print("WARNING: used flag --page, but config option 'page_size' no set. "
                      "Outputted all books.")
                return
        else:
            self._search_paginate(filters, page)

    def _search_books(self, args: Namespace):
        filters = dto.BookFilter(
            title=args.title,
            author=args.author,
            year=args.year,
        )
        page = args.page - 1 if args.page else 0
        self._search_books_common(filters, page)

    def _search_paginate(
        self,
        filters: dto.BookFilter,
        start_page: int,
    ):
        page_size: int = self.config.page_size
        page = start_page

        while True:
            print("---------")

            pagination = Pagination(offset=page * page_size, limit=page_size)

            books = self.service.find_books(filters, pagination)
            for book in books.data:
                print(format_book(book))
                print("---------")

            print(f"Page {page + 1} of {math.ceil(books.pagination.total / page_size)}")
            next_page = books.pagination.next_page
            prev_page = books.pagination.prev_page

            if next_page and prev_page:
                prompt = "Next/Prev (N/P)"
            elif next_page:
                prompt = "Next (N)"
            elif prev_page:
                prompt = "Prev (P)"
            else:
                return

            while True:
                choice = input(f"Select page change: {prompt}: ")
                if len(choice) < 1:
                    print("Invalid choice")
                    continue

                match choice[0].lower():
                    case '>' | 'n':
                        if not next_page:
                            print("Next page not available")
                            continue

                        page += 1
                    case '<' | 'p':
                        if not prev_page:
                            print("Prev page not available")
                            continue

                        page -= 1
                    case _:
                        print("Invalid choice")
                        continue

                os.system('cls' if os.name == 'nt' else 'clear')
                break

    def _all_books(self, args: Namespace):
        page = args.page - 1 if args.page else 0
        self._search_books_common(dto.BookFilter(), page)

    def _bind_commands(self):
        self._handlers.update(
            {
                COMMAND_ADD: self._add_book,
                COMMAND_SEARCH: self._search_books,
                COMMAND_DELETE: self._delete_book,
                COMMAND_ALL: self._all_books,
                COMMAND_STATUS: self._change_status
            }
        )

    def run(self, args: Namespace):
        handler = self._handlers.get(args.cmd)
        if not handler:
            print(f"Unknown command {args.cmd}")
            exit(1)

        handler(args)
