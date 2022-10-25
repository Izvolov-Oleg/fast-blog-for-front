from sqlalchemy import select, insert

from loguru import logger

from app.db.repositories.base import BaseRepository
from app.db.tables import Post
from app.db.errors import UserDoesNotExist
from app.models.schemas.posts import PostSchema, ListOfPosts


class PostRepository(BaseRepository):

    async def create_post(self, user_id: int,
                          title: str,
                          content: str) -> PostSchema:
        q = insert(Post).values(
            title=title,
            author_id=user_id,
            content=content
        ).returning(Post)
        new_post = (await self.session.execute(q)).mappings().one()
        return PostSchema.parse_obj(new_post)

    async def get_all_posts(self, limit: int, offset: int) -> ListOfPosts:
        stmt = select(Post)

