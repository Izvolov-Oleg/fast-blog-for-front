from sqlalchemy import select

from app.db.repositories.base import BaseRepository
from app.db.models import User
from app.db.errors import UserDoesNotExist


class UserRepository(BaseRepository):
    async def get_user_by_username(self, username: str):
        q = await self.session.execute(select(User).where(username=username))
        user = q.scalar_one_or_none()
        if user:
            return user
        raise UserDoesNotExist(f"user with username {username} does not exist")

    async def get_user_by_email(self, email: str):
        q = await self.session.execute(select(User).where(email=email))
        user = q.scalar_one_or_none()
        if user:
            return user
        raise UserDoesNotExist(f"user with email {email} does not exist")

    async def create_user(self, email: str, username: str, password: str) -> User:
        ...
