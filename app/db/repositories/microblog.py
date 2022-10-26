from sqlalchemy import select, insert, func, update, delete
from sqlalchemy.exc import NoResultFound

from loguru import logger

from app.db.repositories.base import BaseRepository
from app.db.tables import Post, Comment, User
from app.db.errors import PostDoesNotExist, CommentDoesNotExist
from app.models.schemas.posts import (
    PostReturnSchema,
    ListOfPosts,
    PostWithAuthorSchema,
    PostWithCommentsSchema
)
from app.models.schemas.comments import (
    CommentWithChildren, CommentReturnSchema,
)


def get_comments_children(comments: list[dict], _id: int | None
                          ) -> list[CommentWithChildren]:
    result = []

    for comment in comments:

        if comment["parent_id"] == _id:
            obj = CommentWithChildren.parse_obj(comment)
            obj.comments = get_comments_children(comments, obj.id)
            result.append(obj)

    return result


class PostRepository(BaseRepository):

    async def create_post(self, user_id: int, title: str, content: str) -> PostReturnSchema:
        q = insert(Post).values(
            title=title,
            author_id=user_id,
            content=content
        ).returning(Post)

        new_post = (await self.session.execute(q)).mappings().one()

        return PostReturnSchema.parse_obj(new_post)

    async def get_all_posts(self, limit: int, offset: int) -> ListOfPosts:
        stmt = select(
            Post.id,
            Post.title,
            Post.content,
            Post.created_at,
            Post.updated_at,
            Post.author_id,
            User.username).join(
            User, Post.author_id == User.id).limit(limit).offset(offset)

        posts_with_user = (await self.session.execute(stmt)).mappings().all()
        total = await self.session.scalar(select(func.count(1)).select_from(Post))

        return ListOfPosts(
            posts=[PostWithAuthorSchema.parse_obj(post) for post in posts_with_user],
            total=total
        )

    async def get_post(self, post_id: int) -> PostWithCommentsSchema:
        try:
            stmt_p = select(
                Post.id,
                Post.title,
                Post.content,
                Post.created_at,
                Post.updated_at,
                Post.author_id,
                User.username).join(
                User, Post.author_id == User.id).where(Post.id == post_id)
            post_orm = (await self.session.execute(stmt_p)).mappings().one()
        except NoResultFound:
            raise PostDoesNotExist(f"Post with id {post_id} does not exist")

        post = PostWithCommentsSchema.parse_obj(post_orm)

        stmt_c = select(
            Comment.id,
            Comment.content,
            Comment.created_at,
            Comment.updated_at,
            Comment.author_id,
            Comment.parent_id,
            User.username,
        ).join(User, Comment.author_id == User.id
               ).where(Comment.post_id == post_id)
        comments = (await self.session.execute(stmt_c)).mappings().all()

        post.comments = get_comments_children(comments, None)
        return post

    async def update_post(self, post_id, **data) -> PostReturnSchema:
        stmt = update(Post).values(**data).where(Post.id == post_id).returning(Post)
        post = (await self.session.execute(stmt)).mappings().one()
        return PostReturnSchema.parse_obj(post)

    async def delete_post(self, post_id) -> None:
        await self.session.execute(delete(Post).where(Post.id == post_id))


class CommentRepository(BaseRepository):

    async def create_comment(
             self, user_id: int,
             content: str,
             post_id: int,
             parent_id: int = None):
        q = insert(Comment).values(
            author_id=user_id,
            content=content,
            post_id=post_id,
            parent_id=parent_id
        ).returning(Comment)
        new_comment = (await self.session.execute(q)).mappings().one()
        await self.session.commit()
        return CommentReturnSchema.parse_obj(new_comment)

    async def get_comment_by_id(self, comment_id) -> CommentReturnSchema:
        try:
            stmt = select(Comment.id,
                          Comment.content,
                          Comment.parent_id,
                          Comment.created_at,
                          Comment.updated_at,
                          Comment.author_id).where(Comment.id == comment_id)
            comment = (await self.session.execute(stmt)).mappings().one()
            return CommentReturnSchema.parse_obj(comment)
        except NoResultFound as e:
            logger.info(str(e))
            raise CommentDoesNotExist(f"Comment with id {comment_id} does not exist")

    async def update_comment(self, comment_id, **data) -> CommentReturnSchema:
        stmt = update(Comment).values(**data).where(Comment.id == comment_id).returning(Comment)
        comment = (await self.session.execute(stmt)).mappings().one()
        return CommentReturnSchema.parse_obj(comment)

    async def delete_comment(self, comment_id) -> None:
        await self.session.execute(delete(Comment).where(Comment.id == comment_id))
