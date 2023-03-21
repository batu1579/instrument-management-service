from typing import Type, TypeVar, Any

from sys import exit as sys_exit

from time import strftime, localtime

from requests.exceptions import ConnectionError as RequestsConnectionError

from loguru import logger

from snowflake import client
from snowflake.server.generator import EPOCH_TIMESTAMP

from app.util.env import SETTINGS
from app.util.type.custom_validator import ValidatedValue


def init_snowflake_client() -> None:
    """初始化 ID 服务客户端"""
    try:
        client.setup(SETTINGS.id_service.host, SETTINGS.id_service.port)
        logger.info(f"id service status: {client.get_stats()}")
    except RequestsConnectionError as error:
        logger.error(f"Can not init id service: {error}")
        sys_exit()


_GuidT = TypeVar("_GuidT", bound="GUID")


class GUID(ValidatedValue[_GuidT]):
    """使用雪花算法生成的全局唯一识别码，依赖于 pysnowflake 生成

    :| 1 bit |                   41 bit                  |   2 bit    |  8 bit   |    12 bit    |
    :|  Sign |                  Timestamp                | DataCenter |  Worker  |   Sequence   |
    :|   0b  | 10000011010101010111000101110110001000110 |     01     | 00010111 | 000000000001 |


    Raises:
        ValueError: GUID 不合法时抛出异常
    """

    __id: int

    def __init__(self, guid: int, need_varification: bool = True):
        """初始化新的 GUID 对象

        Args:
            guid (int): 从服务端获取的 GUID
            need_validate (bool, optional): 是否需要校验. Defaults to True.

        Raises:
            ValueError: _description_
        """
        if need_varification and not GUID.is_valid_guid(guid):
            raise ValueError(f"invalid guid: {guid}")

        self.__id = guid

    @classmethod
    def generate(cls: Type[_GuidT]) -> _GuidT:
        """从服务端获取新的 GUID

        Returns:
            T: 新的 GUID 对象
        """
        return cls(client.get_guid(), need_varification=False)

    @classmethod
    def parse_str(cls: Type[_GuidT], guid: str) -> _GuidT:
        """将 GUID 字符串转换为 GUID 对象

        Args:
            guid (str): GUID 字符串

        Returns:
            T: 新的 GUID 对象
        """
        if not guid.isdigit():
            raise ValueError(f"guid ({guid}) is not a number")
        return cls(int(guid))

    @classmethod
    def __validator__(cls: Type[_GuidT], value: Any) -> _GuidT | None:
        if isinstance(value, int):
            return cls(value)
        if isinstance(value, str):
            return cls.parse_str(value)
        return None

    @classmethod
    def __modify_schema__(cls: Type[_GuidT], field_schema: dict[str, Any]) -> None:
        field_schema.update(
            {
                "type": "string",
                "examples": [
                    cls.generate().guid,
                    cls.generate().to_string(),
                ],
            }
        )

    @property
    def guid(self) -> int:
        """获取数字类型的 GUID

        Returns:
            int: guid
        """
        return self.__id

    @property
    def create_timestamp_ms(self) -> int:
        """获取 GUID 创建时的时间戳

        Returns:
            int: 41 bit 时间戳，单位为毫秒
        """
        return (self.__id >> 22) + EPOCH_TIMESTAMP

    @property
    def create_time_str(self) -> str:
        """获取 GUID 创建时的时间字符串

        Returns:
            str: 时间字符串，格式为： YYYY-MM-DD HH:mm:ss
        """
        time_dict = localtime(int(self.create_timestamp_ms / 1000))
        return strftime("%Y-%m-%d %H:%M:%S", time_dict)

    @property
    def data_center_serial_num(self) -> int:
        """获取生成 GUID 数据中心序号

        Returns:
            int: 2 bit 的序列号
        """
        return self.__id >> 20 & 0x03  # pysnowflake 的实现中使用了 2 bit 的 dc 序列号

    @property
    def worker_serial_num(self) -> int:
        """获取生成 GUID 的机器序列号

        Returns:
            int: 8 bit 的序列号
        """
        return self.__id >> 12 & 0xFF  # pysnowflake 的实现中使用了 8 位的 worker 序列号

    @property
    def sequence_num(self) -> int:
        """获取 GUID 的生成序列号

        Returns:
            int: 12 bit 的序列号
        """
        return self.__id & 0xFFF

    @staticmethod
    def is_valid_guid(guid: int) -> bool:
        """判断 GUID 是否合法

        Args:
            GUID (int): 要检查的 GUID

        Returns:
            bool: 如果合法则返回真
        """
        return guid >> 62 == 1  # 63 位必为 0 且 62 位必为 1

    def to_string(self) -> str:
        """将 GUID 转化为字符串

        用于发送给前端，因为 JS 的 Number 类型最大长度只有 53 位，并不能直接存储 64 位的 GUID 。

        Returns:
            str: 转化后的字符串
        """
        return str(self.__id)

    def get_all_details(self) -> dict[str, str | int]:
        """获取 GUID 的详细信息

        Returns:
            dict[str, str | int]: GUID 包含的全部信息
        """
        return {
            "guid": self.__id,
            "timestamp": self.create_timestamp_ms,
            "time_str": self.create_time_str,
            "data_center": self.data_center_serial_num,
            "worker": self.worker_serial_num,
            "sequence": self.sequence_num,
        }

    def __eq__(self, other: object) -> bool:
        if isinstance(other, GUID):
            return self.__id == other.guid
        if isinstance(other, int):
            return self.__id == other
        if isinstance(other, float):
            return self.__id == int(other)
        if isinstance(other, str):
            return self.to_string() == other
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return f"<GUID: {self.__id}>"

    def __str__(self) -> str:
        return (
            f"<GUID: {self.__id}, "
            + f"Time: {self.create_time_str}>, "
            + f"DC: {self.data_center_serial_num}, "
            + f"Worker: {self.worker_serial_num}, "
            + f"Seq: {self.sequence_num}>"
        )
