from typing import AsyncIterable

from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession

from app.util.env import SETTINGS


class _DataBaseEngine:
    _CONNECT_URL: URL = URL.create(
        drivername="postgresql+asyncpg",
        username=SETTINGS.database.username,
        password=SETTINGS.database.password,
        host=SETTINGS.database.host,
        port=SETTINGS.database.port,
        database=SETTINGS.database.database_name,
        query={
            "charset": "utf8mb4",
        },
    )
    _engine: AsyncEngine
    _session_factory: sessionmaker

    def __init__(self):
        self._engine = create_async_engine(self._CONNECT_URL, echo=True)
        self._session_factory = sessionmaker(
            bind=self._engine,  # type: ignore
            class_=AsyncSession,
            # autoflush=False,
            autocommit=False,
            expire_on_commit=True,
        )

    async def disconnect(self) -> None:
        """断开与数据库的连接"""
        await self._engine.dispose()

    async def get_session(self) -> AsyncIterable[Session]:
        """获取一个与数据库的会话

        Returns:
            Iterable[Session]: 数据库会话
        """
        async with self._session_factory() as session:
            yield session


class _DataBaseClient:
    client: _DataBaseEngine

    def connect_database(self) -> None:
        """连接到数据库"""
        self.client = _DataBaseEngine()

    async def disconnect_database(self) -> None:
        """断开与数据库的连接"""
        if self.client is not None:
            await self.client.disconnect()


DB = _DataBaseClient()
