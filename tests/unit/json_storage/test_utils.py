from src.application.common.pagination import Pagination
from src.infrastructure.db.json.utils import paginate_items


def test_paginate_items():
    source_items = range(1, 11)
    n = len(source_items)

    filtered_items = filter(lambda x: x % 2 == 0, source_items)

    assert paginate_items(Pagination(offset=2, limit=5), n, filtered_items) == [6, 8, 10]
