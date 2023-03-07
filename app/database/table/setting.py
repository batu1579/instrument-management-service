from enum import Enum

from sqlalchemy import Column, String
from sqlalchemy import Enum as SQLAlchemyEnum

from app.database import Base
from app.util.string_length import SHORT_LENGTH, LONG_LENGTH


class SettingValueType(Enum):
    STRING = 0
    INTEGER = 1
    FLOAT = 2
    BOOLEAN = 3


class Setting(Base):
    __tablename__ = "setting"

    value_type = Column(
        SQLAlchemyEnum(SettingValueType),
        nullable=False,
        default=SettingValueType.STRING,
        comment="设置项值类型",
    )
    setting_key = Column(
        String(SHORT_LENGTH), unique=True, nullable=False, comment="设置项名称"
    )
    setting_value = Column(String(LONG_LENGTH), nullable=True, comment="设置项值")
    setting_comment = Column(String(LONG_LENGTH), nullable=True, comment="设置项说明")
