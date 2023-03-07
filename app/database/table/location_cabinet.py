from enum import Enum

from sqlalchemy import Column, String, BigInteger, Integer
from sqlalchemy import Enum as SQLAlchemyEnum

from app.database import Base
from app.util.string_length import SHORT_LENGTH, MIDDLE_LENGTH, LONG_LENGTH


class CabinetStatus(Enum):
    DISABLED = 0
    ENABLED = 1
    FULL_LOAD = 2


class Cabinet(Base):
    __tablename__ = "location_cabinet"

    located_room = Column(BigInteger, nullable=False, comment="所在房间")
    cabinet_name = Column(
        String(SHORT_LENGTH), nullable=False, default="Unnamed Cabinet", comment="存储柜名称"
    )
    cabinet_comment = Column(String(LONG_LENGTH), nullable=True, comment="存储柜备注")
    cabinet_image_url = Column(String(MIDDLE_LENGTH), nullable=True, comment="存储柜图片")

    max_number = Column(Integer, nullable=False, default=0, comment="最大容量")
    current_number = Column(Integer, nullable=False, default=0, comment="当前容量")

    status = Column(
        SQLAlchemyEnum(CabinetStatus),
        nullable=False,
        default=CabinetStatus.DISABLED,
        comment="存储柜状态",
    )
