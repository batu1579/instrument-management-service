from sqlalchemy import Column, BigInteger
from sqlalchemy import Enum as SQLAlchemyEnum

from app.database.table import Base
from app.util.type.enum import ValidatedEnum


class RuleStatus(ValidatedEnum):
    DISABLED = 0
    ENABLED = 1


class StorageLocationType(ValidatedEnum):
    ROOM = 0
    CABINET = 1


class InstrumentStorageRule(Base):
    __tablename__ = "instrument_storage_rule"

    rule_type = Column(
        SQLAlchemyEnum(RuleStatus),
        nullable=False,
        default=RuleStatus.DISABLED,
        comment="规则状态",
    )
    storage_location_type = Column(
        SQLAlchemyEnum(StorageLocationType),
        nullable=False,
        default=StorageLocationType.ROOM,
        comment="存储位置类型",
    )
    storage_location = Column(BigInteger, nullable=False, comment="规则标记的存储位置")
    instrument_category = Column(BigInteger, nullable=False, comment="规则标记的器械类别")
