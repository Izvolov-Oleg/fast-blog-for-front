from fastapi import Query, Path, Depends, HTTPException
from starlette import status

from app.api.dependencies.database import get_repository
from app.db.errors import PostDoesNotExist, CommentDoesNotExist
from app.db.repositories.microblog import PostRepository, CommentRepository
from app.models.schemas.posts import PostFilters, PostWithCommentsSchema
from app.models.schemas.users import User
from app.models.schemas.comments import CommentWithAuthorSchema, CommentReturnSchema
from app.api.dependencies.auth import get_current_user


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


async def get_post_by_id(
        post_id: int = Path(...),
        post_repo: PostRepository = Depends(get_repository(PostRepository))
) -> PostWithCommentsSchema:
    try:
        return await post_repo.get_post(post_id)
    except PostDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not exist"
        )


def check_modify_post_permission(
        current_post: PostWithCommentsSchema = Depends(get_post_by_id),
        user: User = Depends(get_current_user)
) -> None:
    if current_post.author.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not an author of this post",
        )


async def get_comment(
        comment_id: int = Path(...),
        comment_repo: CommentRepository = Depends(get_repository(CommentRepository))
) -> CommentReturnSchema:
    try:
        return await comment_repo.get_comment_by_id(comment_id)
    except CommentDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment does not exist"
        )


def check_modify_comment_permission(
        current_comment: CommentWithAuthorSchema = Depends(get_comment),
        user: User = Depends(get_current_user)
) -> None:
    if current_comment.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not an author of this comments",
        )
