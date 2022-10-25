from fastapi import APIRouter, Depends
from starlette import status

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.database import get_repository
from app.api.dependencies.posts import get_post_filters
from app.db.repositories.microblog import PostRepository
from app.models.schemas.posts import (
    PostCreateSchema,
    PostSchema,
    PostFilters,
    ListOfPosts
)
from app.models.schemas.users import User

router = APIRouter()


@router.get('/', response_model=ListOfPosts)
async def get_all_posts(
        post_filters: PostFilters = Depends(get_post_filters),
        user: User = Depends(get_current_user),  # TODO ????
        post_repo: PostRepository = Depends(get_repository(PostRepository))
):
    ...


@router.post('/', response_model=PostSchema, status_code=status.HTTP_201_CREATED)
async def create_post(
        post_create: PostCreateSchema,
        user: User = Depends(get_current_user),
        post_repo: PostRepository = Depends(get_repository(PostRepository))
):
    return await post_repo.create_post(user.id,
                                       post_create.title,
                                       post_create.content)

