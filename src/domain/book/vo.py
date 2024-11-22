from enum import StrEnum, auto


class BookStatus(StrEnum):
    # Book in available in library
    AVAILABLE = auto()

    # Book was taken from library
    TAKEN = auto()
