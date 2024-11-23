from argparse import ArgumentParser

from src.application.book.service import Service
from src.presentation.cli.cli import COMMAND_ALL, COMMAND_STATUS, COMMAND_SEARCH, COMMAND_DELETE, COMMAND_ADD, CLI
from src.infrastructure.config_loader import load_config
from src.infrastructure.db.json import FileJsonProvider, JsonStorage


def _build_parser():
    parser = ArgumentParser(
        description="Book library system",
    )
    parser.add_argument("--config",
                        type=str, help="Path to config file", default="configs/config.ini")
    subparsers = parser.add_subparsers(dest="cmd")

    # Команда добавления книги
    parser_add = subparsers.add_parser(
        name=COMMAND_ADD,
        help='Add book',
        description="Adds book. Title, author and year are required"

    )
    parser_add.add_argument('title', type=str, help='Book title')
    parser_add.add_argument('author', type=str, help='Author of the book')
    parser_add.add_argument('year', type=int, help='Year of publication')
    # parser_add.set_defaults(func=self._add_book)

    # Команда удаления книги
    parser_delete = subparsers.add_parser(
        name=COMMAND_DELETE,
        help='Delete book',
        description="Delete book by id"
    )
    parser_delete.add_argument('id', type=int, help='Book id')
    # parser_delete.set_defaults(func=self._delete_book)

    # Команда поиска книг
    parser_search = subparsers.add_parser(
        name=COMMAND_SEARCH,
        help='Search books',
        description='Search books by title, author or year'
    )

    parser_search.add_argument('--title', type=str, help='Book title', default=None)
    parser_search.add_argument('--author', type=str, help='Author of the book', default=None)
    parser_search.add_argument('--year', type=int, help='Year of publication', default=None)
    parser_search.add_argument(
        "--page",
        type=int,
        help="Number of page. Available only in set page_size in config",
        default=1,
    )
    # parser_search.set_defaults(func=self._search_books)

    parser_all = subparsers.add_parser(
        name=COMMAND_ALL,
        help="Output all books",
        description="Output all books."
    )
    parser_all.add_argument(
        "--page",
        type=int,
        help="Number of page. Available only in set page_size in config",
    )

    # Команда изменения статуса книги
    parser_status = subparsers.add_parser(
        name=COMMAND_STATUS,
        help='Change book status',
        description="Change book status by id"
    )
    parser_status.add_argument('id', type=int, help='Book id')
    group = parser_status.add_mutually_exclusive_group(required=True)
    group.add_argument("--return", action='store_true', dest="status", help="Set available status")
    group.add_argument("--take", action='store_false', dest="status", help="Set taken status")

    # parser_status.set_defaults(func=self._change_status)

    return parser


def main():
    parser = _build_parser()
    args = parser.parse_args()

    if not hasattr(args, 'cmd') or args.cmd is None:
        parser.print_help()
        exit(0)

    config = load_config(args.config)
    provider = FileJsonProvider(config.storage_path)
    repo = JsonStorage(provider)
    service = Service(repo)

    cli = CLI(config, service)
    cli.run(args)
