from fastapi import Query

from app.models.schemas.posts import PostFilters

DEFAULT_POST_LIMIT = 20
DEFAULT_POST_OFFSET = 0


def get_post_filters(
        offset: int = Query(DEFAULT_POST_OFFSET, ge=0),
        limit: int = Query(DEFAULT_POST_LIMIT, ge=1)
) -> PostFilters:
    return PostFilters(
        offset=offset,
        limit=limit
    )
