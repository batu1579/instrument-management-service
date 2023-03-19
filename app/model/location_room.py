from typing import Optional

from pydantic import Field, HttpUrl

from app.model.response import Success
from app.model.base import DataModel, InCreateModel, InUpdateModel
from app.util.regex_pattern import NAME_PATTERN
from app.util.string_length import SHORT_LENGTH, LONG_LENGTH, URL_LENGTH


class _BaseRoom(DataModel):
    room_name: str = Field(
        ...,
        max_length=SHORT_LENGTH,
        regex=NAME_PATTERN,
        title="房间名称",
        description="用来区分房间，只能使用中文、大小写字母、数字、下划线、中划线，默认为 Unnamed Room",
        example="Room_1",
    )
    room_comment: Optional[str] = Field(
        None,
        max_length=LONG_LENGTH,
        title="房间备注",
        example="This is a room comment",
    )
    room_image_url: Optional[HttpUrl] = Field(
        None,
        max_length=URL_LENGTH,
        title="房间图片的 URL",
        example="https://example.com/image.png",
    )


class Room(_BaseRoom):
    pass


class RoomInCreate(InCreateModel, _BaseRoom):
    room_name: Optional[str] = Field(
        "Unnamed Room",
        max_length=SHORT_LENGTH,
        regex=NAME_PATTERN,
        title="房间名称",
        description="用来区分房间，只能使用中文、大小写字母、数字、下划线、中划线，默认为 Unnamed Room",
        example="Room_1",
    )


class RoomInUpdate(InUpdateModel, _BaseRoom):
    room_name: Optional[str] = Field(
        None,
        max_length=SHORT_LENGTH,
        regex=NAME_PATTERN,
        title="房间名称",
        description="用来区分房间，只能使用中文、大小写字母、数字、下划线、中划线，默认为 Unnamed Room",
        example="Room_1",
    )


class RoomInResponse(Success):
    data: list[Room]
