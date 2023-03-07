from sqlalchemy import Column, BigInteger, DateTime

from app.database import Base


class Instrument(Base):
    __tablename__ = "instruments"

    loacted_cabinet = Column(BigInteger, nullable=False, comment="所在存储柜")
    instrument_category = Column(BigInteger, nullable=False, comment="所属分类")

    expire_time = Column(DateTime, comment="过期时间")  # 与器械分类中的过期时间一致， Null 表示永不过期
