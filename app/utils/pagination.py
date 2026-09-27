from typing import Tuple
from fastapi import Query


def get_pagination_params(
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    limit: int = Query(default=24, ge=1, le=100, description="Items per page (max 100)")
) -> Tuple[int, int]:
    """Calculate offset and validated limit for SQL query."""
    safe_limit = min(max(1, limit), 100)
    offset = (page - 1) * safe_limit
    return offset, safe_limit
