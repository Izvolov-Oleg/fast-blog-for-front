from sqlalchemy import select

from app.db.repositories.base import BaseRepository
from app.db.errors import UserDoesNotExist
from app.db.tables import User


class UserRepository(BaseRepository):
    async def get_user_by_username(self, username: str) -> User:
        q = await self.session.execute(select(User).where(User.username == username))
        user = q.scalar_one_or_none()
        if user:
            return user
        raise UserDoesNotExist(f"user with username {username} does not exist")

    async def get_user_by_email(self, email: str) -> User:
        q = await self.session.execute(select(User).where(User.email == email))
        user = q.scalar_one_or_none()
        if user:
            return user
        raise UserDoesNotExist(f"user with email {email} does not exist")

    async def create_user(self, email: str, username: str, password: str) -> User:
        new_user = User(
            email=email,
            username=username,
            password=password
        )
        self.session.add(new_user)
        await self.session.commit()
        return new_user
