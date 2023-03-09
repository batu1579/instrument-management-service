from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, DateTime, func


class Base(declarative_base()):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, index=True)

    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.id}>"
