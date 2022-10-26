from datetime import datetime

from pydantic import BaseModel, Field, root_validator
from app.models.schemas.users import User


class CommentSchema(BaseModel):
    content: str


class CommentCreateSchema(CommentSchema):
    parent_id: int | None = Field(..., ge=1)


class CommentReturnSchema(CommentCreateSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    author_id: int | None


class CommentWithAuthorSchema(CommentReturnSchema):
    author: User

    @root_validator(pre=True)
    def get_author(cls, values):
        if not values.get('author'):
            values['author'] = User(
                id=values['author_id'],
                username=values['username']
            )
        return values


class CommentWithChildren(CommentWithAuthorSchema):
    comments: list['CommentWithChildren'] | None


class CommentUpdateSchema(CommentSchema):
    ...
