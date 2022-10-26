from typing import AsyncGenerator, Type, Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import async_session
from app.db.repositories.base import BaseRepository


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session
        await session.commit()


def get_repository(repo_type: Type[BaseRepository]) -> Callable:
    def _get_repo(session: AsyncSession = Depends(get_session)
                  ) -> BaseRepository:
        return repo_type(session)
    return _get_repo
