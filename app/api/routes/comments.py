from fastapi import APIRouter, Depends, Response
from starlette import status

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.database import get_repository
from app.api.dependencies.posts import (
    check_modify_comment_permission,
    get_post_by_id
)
from app.db.repositories.microblog import CommentRepository
from app.models.schemas.posts import PostWithCommentsSchema
from app.models.schemas.comments import (
    CommentCreateSchema,
    CommentUpdateSchema, CommentReturnSchema
)
from app.models.schemas.users import User

router = APIRouter()


@router.post('/', response_model=CommentReturnSchema, status_code=status.HTTP_201_CREATED)
async def create_comment(
        comment_create: CommentCreateSchema,
        post: PostWithCommentsSchema = Depends(get_post_by_id),
        user: User = Depends(get_current_user),
        comment_repo: CommentRepository = Depends(get_repository(CommentRepository))
):
    return await comment_repo.create_comment(
        user_id=user.id,
        content=comment_create.content,
        parent_id=comment_create.parent_id,
        post_id=post.id
    )


@router.put(
    "/{comment_id}/",
    response_model=CommentCreateSchema,
    dependencies=[Depends(check_modify_comment_permission), Depends(get_post_by_id)]
)
async def update_comment(
        comment_id: int,
        comment_update: CommentUpdateSchema,
        comment_repo: CommentRepository = Depends(get_repository(CommentRepository))
):
    return await comment_repo.update_comment(comment_id, **comment_update.dict())


@router.delete(
    "/{comment_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    dependencies=[Depends(check_modify_comment_permission), Depends(get_post_by_id)]
)
async def delete_post(
        comment_id: int,
        comment_repo: CommentRepository = Depends(get_repository(CommentRepository))
):
    await comment_repo.delete_comment(comment_id)
