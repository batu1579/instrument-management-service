from sqlalchemy import Column, String

from app.database import Base
from app.util.string_length import SHORT_LENGTH, LONG_LENGTH


class Setting(Base):
    __tablename__ = "setting"

    setting_key = Column(
        String(SHORT_LENGTH), unique=True, nullable=False, comment="设置项名称"
    )
    setting_value = Column(String(SHORT_LENGTH), nullable=False, comment="设置项值")
    setting_comment = Column(String(LONG_LENGTH), nullable=True, comment="设置项说明")
