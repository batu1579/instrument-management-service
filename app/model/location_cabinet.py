from typing import Optional

from pydantic import Field, HttpUrl, validator

from app.model.response import Success
from app.model.base import DataModel, InCreateModel, InUpdateModel
from app.database.table.location_cabinet import CabinetStatus
from app.util.type.guid import GUID
from app.util.regex_pattern import NAME_PATTERN
from app.util.string_length import SHORT_LENGTH, LONG_LENGTH, URL_LENGTH


class _BaseCabinet(DataModel):
    located_room: GUID = Field(
        ...,
        title="存储柜所在房间的 ID",
        example=GUID.generate().guid,
    )
    cabinet_name: str = Field(
        ...,
        max_length=SHORT_LENGTH,
        regex=NAME_PATTERN,
        title="存储柜名称",
        description="用来区分存储柜，只能使用中文、大小写字母、数字、下划线、中划线，默认为 Unnamed Cabinet",
        example="Cabinet_1",
    )
    cabinet_comment: Optional[str] = Field(
        None,
        max_length=LONG_LENGTH,
        title="存储柜备注",
        example="Some comment of the cabinet",
    )
    cabinet_image_url: Optional[HttpUrl] = Field(
        None,
        max_length=URL_LENGTH,
        title="存储柜图片的 URL",
        example="http://www.example.com/image.png",
    )
    max_number: int = Field(
        ...,
        gt=0,
        title="存储柜最大容量",
        description="存储柜最多能存放的物品数量，如果不希望被限制可以尝试使用一个非常大的数值",
        example=9999,
    )
    current_number: int = Field(
        ...,
        gt=0,
        title="存储柜当前容量",
        description="当前容量不能超过最大值，且当达到最大时会更新存储柜状态为满载",
        example=100,
    )
    status: CabinetStatus = Field(
        ...,
        title="存储柜状态",
        description="""
        可选的存储柜状态为：
        
            - DISABLED  (0): 禁用
            - ENABLED   (1): 启用
            - FULL_LOAD (2): 满载
            
        新建立的存储柜默认为禁用（ DISABLED ）。""",
        example=CabinetStatus.DISABLED,
    )

    @validator("current_number")
    def check_current_number(cls, value: int, values: dict) -> int:
        """检查存储柜当前容量

        Args:
            value (int): 当前容量
            values (dict): 模型全部字段

        Raises:
            ValueError: 当当前容量大于最大容量时抛出异常

        Returns:
            int: 当前容量
        """
        max_number: int | None = values.get("max_number")

        assert max_number is not None, "max_number is required"

        if value > max_number:
            raise ValueError(
                f"current_number ({value}) is greater than max_number ({max_number})"
            )
        return value

    @validator("status")
    def check_status(cls, value: CabinetStatus, values: dict) -> CabinetStatus:
        """检查存储柜状态

        Args:
            value (CabinetStatus): 当前的状态
            values (dict): 模型全部字段

        Raises:
            ValueError: 当输入的状态不支持时抛出异常

        Returns:
            CabinetStatus: 存储柜状态
        """
        max_number: int | None = values.get("max_number")
        current_number: int | None = values.get("current_number")

        assert max_number is not None, "max_number is required"
        assert current_number is not None, "current_number is required"

        if max_number == current_number:
            return CabinetStatus.FULL_LOAD
        return value


class Cabinet(_BaseCabinet):
    pass


class CabinetInCreate(InCreateModel, _BaseCabinet):
    cabinet_name: Optional[str] = Field(
        "Unnamed Cabinet",
        max_length=SHORT_LENGTH,
        regex=NAME_PATTERN,
        title="存储柜名称",
        description="用来区分存储柜，只能使用中文、大小写字母、数字、下划线、中划线，默认为 Unnamed Cabinet",
        example="Cabinet_1",
    )
    current_number: Optional[int] = Field(
        0,
        title="存储柜当前容量",
        description="当前容量不能超过最大值，且当达到最大时会更新存储柜状态为满载",
        example=100,
    )
    status: Optional[CabinetStatus] = Field(
        CabinetStatus.DISABLED,
        title="存储柜状态",
        description="""
        可选的存储柜状态为：
        
            - DISABLED  (0): 禁用
            - ENABLED   (1): 启用
            - FULL_LOAD (2): 满载
            
        新建立的存储柜默认为禁用（ DISABLED ）。""",
        example=CabinetStatus.DISABLED,
    )


class CabinetInUpdate(InUpdateModel, _BaseCabinet):
    located_room: Optional[GUID] = Field(
        None,
        title="存储柜所在房间的 ID",
        example=GUID.generate().guid,
    )
    cabinet_name: Optional[str] = Field(
        None,
        max_length=SHORT_LENGTH,
        regex=NAME_PATTERN,
        title="存储柜名称",
        description="用来区分存储柜，只能使用中文、大小写字母、数字、下划线、中划线，默认为 Unnamed Cabinet",
        example="Cabinet_1",
    )
    cabinet_comment: Optional[str] = Field(
        None,
        max_length=LONG_LENGTH,
        title="存储柜备注",
        example="Some comment of the cabinet",
    )
    cabinet_image_url: Optional[HttpUrl] = Field(
        None,
        max_length=URL_LENGTH,
        title="存储柜图片的 URL",
        example="http://www.example.com/image.png",
    )
    max_number: Optional[int] = Field(
        None,
        gt=0,
        title="存储柜最大容量",
        description="存储柜最多能存放的物品数量，如果不希望被限制可以尝试使用一个非常大的数值",
        example=9999,
    )
    current_number: Optional[int] = Field(
        None,
        gt=0,
        title="存储柜当前容量",
        description="当前容量不能超过最大值，且当达到最大时会更新存储柜状态为满载",
        example=100,
    )
    status: Optional[CabinetStatus] = Field(
        None,
        title="存储柜状态",
        description="""
        可选的存储柜状态为：
        
            - DISABLED  (0): 禁用
            - ENABLED   (1): 启用
            - FULL_LOAD (2): 满载
            
        新建立的存储柜默认为禁用（ DISABLED ）。""",
        example=CabinetStatus.DISABLED,
    )


class CabinetInResponse(Success):
    data: list[Cabinet]
