from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings


engine = create_async_engine(settings.database_url, echo=False)

# TODO определдать класс Base для моделс


# это перенести в файл dependencies
async def get_session() -> AsyncGenerator:
    # а это вытащить из функции
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session
