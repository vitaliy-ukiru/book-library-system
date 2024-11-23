from typing import Iterable, TypeVar

from src.application.common.pagination import Pagination


T = TypeVar("T")

def paginate_items(
    pagination: Pagination,
    total_count: int,
    filtered_items: Iterable[T]
) -> list[T]:
    """
    Optimized pagination of items stream.

    :param pagination: Pagination rules object
    :param total_count: Total count of items in source container.
    :param filtered_items: Filtered iterator of items.
    :return: A paginated list of items.
    """
    offset = pagination.offset or 0
    limit = pagination.limit if pagination.limit else total_count

    items = []
    for i, item in enumerate(filtered_items):
        if i >= offset:
            items.append(item)

        if len(items) >= limit:
            break

    return items
