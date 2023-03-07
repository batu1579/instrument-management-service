from typing import Iterable

from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, BigInteger, DateTime, func

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
        drivername="mysql+pymysql",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        query={
            "charset": "utf8mb4",
        },
    )
    _engine: Engine
    _session_factory: sessionmaker

    def __init__(self):
        self._engine = create_engine(self._CONNECT_URL, encoding="utf-8", echo=True)
        self._session_factory = sessionmaker(
            bind=self._engine,
            # autoflush=False,
            autocommit=False,
            expire_on_commit=True,
        )

    def disconnect(self) -> None:
        """断开与数据库的连接"""
        self._engine.dispose()

    def get_session(self) -> Iterable[Session]:
        """获取一个与数据库的会话

        Returns:
            Iterable[Session]: 数据库会话
        """
        with self._session_factory() as session:
            yield session


class _DataBaseClient:
    client: _DataBaseEngine

    def connect_database(self) -> None:
        """连接到数据库"""
        self.client = _DataBaseEngine()

    def disconnect_database(self) -> None:
        """断开与数据库的连接"""
        if self.client is not None:
            self.client.disconnect()


DB = _DataBaseClient()
