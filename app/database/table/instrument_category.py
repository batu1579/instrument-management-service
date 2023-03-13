from sqlalchemy import Column, String, BigInteger

from app.database.table import Base
from app.util.string_length import SHORT_LENGTH, MIDDLE_LENGTH, LONG_LENGTH


class InstrumentCategory(Base):
    __tablename__ = "instrument_category"

    category_name = Column(
        String(SHORT_LENGTH),
        nullable=False,
        default="Unnamed Instrument",
        comment="器械名称",
    )
    category_comment = Column(String(LONG_LENGTH), nullable=True, comment="器械备注")
    category_image_url = Column(String(MIDDLE_LENGTH), nullable=True, comment="器械图片")

    expire_duration_MS = Column(BigInteger, comment="过期时长")  # 设为 Null 时代表永不过期
