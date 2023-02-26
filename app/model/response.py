from typing import Optional, Generic, TypeVar

from abc import ABC

from pydantic import HttpUrl
from pydantic.generics import GenericModel

from app.model.base import BaseModel

DataField = TypeVar("DataField", BaseModel, str)


class Response(BaseModel, ABC):
    """响应数据模型

    Args:
        status (int): 响应状态 (1 为成功， -1 为失败)
        code (int): 状态码
        msg (str): 相应描述信息
    """

    status: int
    code: int
    msg: str


class Success(GenericModel, Generic[DataField], Response):
    """成功响应模型

    Args:
        status (int): 响应状态 (必为 1)
        code (Optional[int]): 状态码 (默认为 200)
        msg (Optional[str]): 详细错误信息 (默认为 Success)
        data (DataField): 响应附带的数据
    """

    status: int = 1
    code: Optional[int] = 200
    msg: Optional[str] = "Success"
    data: DataField


class Error(Response):
    """失败响应模型

    Args:
        status (int): 响应状态 (必为 -1)
        code (int): 错误码
        msg (str): 详细错误信息
        data (str): 响应附带的数据 (必为空字符串)
        info (str | HttpUrl | dict): 错误码对应的文档或帮助信息
    """

    status: int = -1
    data: str = ""
    info: str | HttpUrl | dict
