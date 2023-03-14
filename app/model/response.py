from typing import Optional

from abc import ABC

from pydantic import HttpUrl, Field, validator

from app.model.base import BaseModel


class Response(BaseModel, ABC):
    """响应数据模型

    Args:
        status (int): 响应状态 (0 为成功， 1 为失败)
        code (int): 状态码
        msg (str): 相应描述信息
        info (Optional[str | HttpUrl | dict]): 附加的说明信息
    """

    status: int
    code: int
    msg: str
    info: Optional[str | HttpUrl | dict] = Field(
        "",
        title="附加的说明信息",
        description="错误码对应的文档、帮助信息或其他对于接口的说明信息",
        examples=[
            "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404",
            "This interface is deprecated, please use the following path: example.com/v2 ."
            + "For more information see the documentation: example.com/docs .",
        ],
    )


class Success(Response):
    """成功响应模型

    Args:
        status (Optional[int]): 响应状态 (必为 0)
        code (Optional[int]): 状态码 (必为 200)
        msg (Optional[str]): 详细错误信息 (必为 Success)
        data (list[BaseModel | dict]): 响应附带的数据
        data_length (Optional[int]): 相应附带的数据长度
        info (Optional[str | HttpUrl]): 附加的说明信息
    """

    status: Optional[int] = Field(
        0,
        const=True,
        title="响应状态",
        description="因为是成功的响应，所以状态必定为 0",
    )
    code: Optional[int] = Field(
        200,
        const=True,
        title="状态码",
        description="因为是成功的响应，状态码必定为 200",
    )
    msg: Optional[str] = Field(
        "Success",
        const=True,
        title="响应消息",
        description="因为是成功的响应，响应消息必定为 Success 。如果有需要告知的额外信息，请使用 info 字段",
    )
    data: list[BaseModel | dict] = Field(
        {},
        title="响应附带的数据",
        description="可能是单条数据或多条数据组成的列表",
    )
    data_length: Optional[int] = Field(
        None,
        title="数据条目数量",
        description="携带的数据条数",
    )

    @validator("data_length", always=True)
    def add_data_length(cls, _, values: dict) -> Optional[int]:
        """为携带多条数据的相应添加数据条数信息

        Args:
            values (dict): 包含的全部信息

        Returns:
            Optional[int]: 携带的数据条数
        """
        return len(values.get("data"))  # type: ignore


class Error(Response):
    """失败响应模型

    Args:
        status (int): 响应状态 (必为 1)
        code (int): 错误码
        msg (str): 详细错误信息
        data (str): 响应附带的数据 (必为空字符串)
        info (str | HttpUrl | dict): 错误码对应的文档或帮助信息
    """

    status: Optional[int] = Field(
        1,
        const=True,
        title="响应状态",
        description="因为是失败的响应，所以状态必定为 1",
    )
    code: int = Field(
        ...,
        ge=300,
        title="错误码",
        description="产生异常的错误码，用于快速找到异常原因。使用的错误码与 HTTP 状态码对应",
        example=404,
    )
    msg: str = Field(
        ...,
        title="响应消息",
        description="详细错误信息",
    )
    data: Optional[dict] = Field(
        [],
        const=True,
        title="响应附带的数据",
        description="因为是失败的响应，所以不能携带数据",
    )
    data_length: Optional[int] = Field(
        0,
        const=True,
        title="数据条目数量",
        description="携带的数据条数",
    )
