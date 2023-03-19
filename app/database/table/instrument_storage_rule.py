from sqlalchemy import Column, String
from sqlalchemy import Enum as SQLAlchemyEnum

from app.database.table import Base
from app.util.type.enum import ValidatedEnum
from app.util.string_length import SHORT_LENGTH, LONG_LENGTH


class RuleStatus(ValidatedEnum):
    DISABLED = 0
    ENABLED = 1


class RuleType(ValidatedEnum):
    ALL_FORBID = 0
    BLACK_LIST = 1
    WHITE_LIST = 2


class InstrumentStorageRule(Base):
    __tablename__ = "instrument_storage_rule"

    rule_name = Column(
        String(SHORT_LENGTH),
        nullable=False,
        default="Unnamed Storage Rule",
        comment="存储规则名称",
    )
    rule_status = Column(
        SQLAlchemyEnum(RuleStatus),
        nullable=False,
        default=RuleStatus.DISABLED,
        comment="存储规则状态",
    )
    rule_type = Column(
        SQLAlchemyEnum(RuleType),
        nullable=False,
        default=RuleType.ALL_FORBID,
        comment="存储规则类型",
    )
    rule_comment = Column(
        String(LONG_LENGTH),
        nullable=True,
        comment="存储规则备注",
    )
