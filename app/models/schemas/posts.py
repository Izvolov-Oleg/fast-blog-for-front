from datetime import datetime

from pydantic import BaseModel

from app.models.schemas.users import User

# class PostBase(BaseModel):
#     content: str


class PostCreateSchema(BaseModel):
    title: str
    content: str


class PostSchema(BaseModel):
    id: int
    title: str
    author_id: int
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PostFilters(BaseModel):
    limit: int
    offset: int


class ListOfPosts(BaseModel):
    posts: list[PostSchema]
    posts_count: int
