from sqlalchemy import Column, BigInteger
from sqlalchemy import Enum as SQLAlchemyEnum

from app.database.table import Base
from app.util.type.enum import ValidatedEnum


class StorageLocationType(ValidatedEnum):
    ROOM = 0
    CABINET = 1


class StorageRuleRecord(Base):
    __tablename__ = "storage_rule_record"

    storage_rule = Column(BigInteger, nullable=False, comment="所属的存储规则")
    storage_location_type = Column(
        SQLAlchemyEnum(StorageLocationType),
        nullable=False,
        default=StorageLocationType.ROOM,
        comment="存储位置类型",
    )
    storage_location = Column(BigInteger, nullable=False, comment="规则标记的存储位置")
    instrument_category = Column(BigInteger, nullable=False, comment="规则标记的器械类别")
