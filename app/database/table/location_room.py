from sqlalchemy import Column, String

from app.database import Base
from app.util.string_length import SHORT_LENGTH, MIDDLE_LENGTH, LONG_LENGTH


class Room(Base):
    __tablename__ = "location_room"

    room_name = Column(
        String(SHORT_LENGTH), nullable=False, default="Unnamed Room", comment="房间名称"
    )
    room_comment = Column(
        String(LONG_LENGTH), nullable=True, default="", comment="房间备注"
    )
    room_image_url = Column(String(MIDDLE_LENGTH), nullable=True, comment="房间图片")
