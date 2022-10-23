from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, async_session: AsyncSession) -> None:
        self._session = async_session

    @property
    def session(self) -> AsyncSession:
        return self._session
