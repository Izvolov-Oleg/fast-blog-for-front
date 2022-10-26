from fastapi import APIRouter, Depends, Response
from starlette import status

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.database import get_repository
from app.api.dependencies.posts import \
    (get_post_filters,
     get_post_by_id,
     check_modify_post_permission
     )
from app.db.repositories.microblog import PostRepository
from app.models.schemas.posts import (
    PostCreateSchema,
    PostReturnSchema,
    PostFilters,
    ListOfPosts,
    PostWithCommentsSchema,
    PostUpdateSchema
)
from app.models.schemas.users import User

router = APIRouter()


@router.get('/', response_model=ListOfPosts)
async def get_all_posts(
        post_filters: PostFilters = Depends(get_post_filters),
        post_repo: PostRepository = Depends(get_repository(PostRepository))
):
    return await post_repo.get_all_posts(post_filters.limit, post_filters.offset)


@router.get('/{post_id}/', response_model=PostWithCommentsSchema)
async def get_post(
        post: PostWithCommentsSchema = Depends(get_post_by_id)
):
    return post


@router.post('/', response_model=PostReturnSchema, status_code=status.HTTP_201_CREATED)
async def create_post(
        post_create: PostCreateSchema,
        user: User = Depends(get_current_user),
        post_repo: PostRepository = Depends(get_repository(PostRepository))
):
    return await post_repo.create_post(
        user.id, post_create.title, post_create.content
    )


@router.put(
    "/{post_id}/",
    response_model=PostReturnSchema,
    dependencies=[Depends(check_modify_post_permission)]
)
async def update_post(
        post_id: int,
        post_update: PostUpdateSchema,
        post_repo: PostRepository = Depends(get_repository(PostRepository))
):
    return await post_repo.update_post(post_id, **post_update.dict())


@router.delete(
    "/{post_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    dependencies=[Depends(check_modify_post_permission)]
)
async def delete_post(
        post_id: int,
        post_repo: PostRepository = Depends(get_repository(PostRepository))
):
    await post_repo.delete_post(post_id)
