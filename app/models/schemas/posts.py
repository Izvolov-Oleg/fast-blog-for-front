from datetime import datetime

from pydantic import BaseModel
from pydantic.class_validators import root_validator

from app.models.schemas.users import User
from app.models.schemas.comments import CommentWithChildren


class PostCreateSchema(BaseModel):
    title: str
    content: str


class PostSchema(PostCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class PostReturnSchema(PostSchema):
    author_id: int


class PostWithAuthorSchema(PostSchema):
    author: User

    @root_validator(pre=True)
    def get_author(cls, values):
        if not values.get('author'):
            values['author'] = User(
                id=values['author_id'],
                username=values['username']
            )
        return values


class PostWithCommentsSchema(PostWithAuthorSchema):
    comments: list[CommentWithChildren] | None


class PostFilters(BaseModel):
    limit: int
    offset: int


class ListOfPosts(BaseModel):
    posts: list[PostWithAuthorSchema]
    total: int


class PostUpdateSchema(BaseModel):
    content: str
