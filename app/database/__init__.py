from typing import AsyncIterable

from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, BigInteger, DateTime, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession

from app.util.env import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
)


class Base(declarative_base()):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, index=True)

    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.id}>"


class _DataBaseEngine:
    _CONNECT_URL: URL = URL.create(
        drivername="postgresql+asyncpg",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
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
