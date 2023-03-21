from typing import Optional, Any, TypeVar, Type

from pathlib import Path

from pydantic import BaseSettings, Field, validator

from starlette.datastructures import CommaSeparatedStrings

from loguru import logger


class _ServiceSettings(BaseSettings):
    host: str = Field(
        "localhost",
        title="服务主机地址",
        examples=["localhost", "127.0.0.1"],
    )
    port: int = Field(8081, gt=0, title="服务端口")

    keyfile_path: Optional[Path] = Field(None, title="密钥文件路径")
    certfile_path: Optional[Path] = Field(None, title="证书文件路径")
    use_https_only: Optional[str | bool] = Field(False, title="是否使用中间件重定向所有请求到https")

    origins: Optional[list[str] | str] = Field(
        [
            "http://localhost",
            "https://localhost",
        ],
        title="信任的域名列表",
    )

    gzip_min_size: Optional[int] = Field(500, ge=0, title="开始使用 GZIP 压缩的最小大小")

    @staticmethod
    def __transform_relative_path(path: Optional[Path]) -> Optional[Path]:
        """将相对文件路径转换为绝对路径

        Args:
            path (Optional[str]): 文件路径

        Returns:
            Optional[str]: 绝对文件路径（当传入为 None 时也返回 None ）。·
        """
        if path is None:
            return None
        if not path.is_file():
            logger.warning(f"{path} is not a file. Please check.")
            return None
        if not path.is_absolute():
            return path.absolute()
        return path

    transform_keyfile_path = validator(
        "keyfile_path", allow_reuse=True, check_fields=False
    )(__transform_relative_path)
    transform_certfile_path = validator(
        "certfile_path", allow_reuse=True, check_fields=False
    )(__transform_relative_path)

    @validator("use_https_only", check_fields=False)
    def check_bool(cls, value: str | bool) -> bool:
        """校验 https 重定向设置

        Args:
            value (str | bool): 是否启用 https 重定向

        Returns:
            bool: 是否启用 https 重定向
        """
        if isinstance(value, bool):
            return value
        return value.lower() == "true"

    @validator("user_https_only", check_fields=False)
    def check_file_path(cls, value: bool, values: dict) -> bool:
        """检查设置的密钥文件和证书文件是否存在

        Args:
            value (bool): 是否启用 https 重定向
            values (dict): 模型全部字段数据

        Returns:
            bool: 是否启用 https 重定向（不符合要求会强行修改为禁用重定向，并且记录入日志）
        """
        keyfile_path: Path | None = values.get("keyfile_path")
        certfile_path: Path | None = values.get("certfile_path")

        if value is False:
            return value

        if keyfile_path is None or certfile_path is None:
            logger.warning(
                "If you want to enable https redirection, "
                + "you need to set keyfile_path and certfile_path both. "
                + "Now https redirection will be disabled."
            )
            return False

        keyfile_path = Path(keyfile_path)
        certfile_path = Path(certfile_path)

        if not keyfile_path.exists():
            logger.warning(
                f"Can not find keyfile at {keyfile_path}. "
                + "Please check the file or settings spell. "
                + "Now https redirection will be disabled."
            )
            return False

        if not certfile_path.exists():
            logger.warning(
                f"Can not find certfile at {certfile_path}. "
                + "Please check the file or settings spell. "
                + "Now https redirection will be disabled."
            )
            return False

        return True

    @validator("origins", check_fields=False)
    def check_origins(cls, value: list[str] | str) -> list[str]:
        """校验信任的域名列表

        Args:
            value (list[str] | str): 信任的域名列表

        Returns:
            list[str]: 将字符串列表准换为字符串对象
        """
        if isinstance(value, str):
            return list(map(lambda x: str(), CommaSeparatedStrings(value)))
        return value

    class Config:
        fields: dict[str, dict[str, str]] = {
            "keyfile_path": {"env": "KEYFILE"},
            "certfile_path": {"env": "CERTFILE"},
        }


class _DatabaseSettings(BaseSettings):
    host: Optional[str] = Field(
        "localhost",
        title="数据库主机地址",
        examples=["localhost", "127.0.0.1"],
    )
    port: Optional[int] = Field(3306, gt=0, title="数据库端口")

    username: str = Field(
        ...,
        title="访问数据库的用户名",
        description="用于访问数据库中的记录。强烈建议不要使用超级权限用户，应选择只给予了特定数据库读写权限的用户",
    )
    password: str = Field(..., title="访问数据库的用户密码")

    database_name: str = Field(..., title="使用的数据库名")

    class Config:
        env_prefix = "DB_"
        fields: dict[str, dict[str, str]] = {
            "database_name": {
                "env": "DB_NAME",
            },
        }


class _DocsSettings(BaseSettings):
    docs_title: str = Field("Service Docs", title="文档标题")

    docs_path: Path = Field(
        "/docs",
        title="交互文档路径",
        description="主机地址与服务地址相同，文档由 Swagger UI 提供",
    )
    redocs_path: Path = Field(
        "/redocs",
        title="替代文档路径",
        description="主机地址与服务地址相同，文档由 ReDocs 提供",
    )


class _LogSettings(BaseSettings):
    rotation: Optional[str] = Field(
        "200 MB",
        title="日志分隔方式",
        examples=[
            "0.5 GB",
            "200 MB",
            "4 days",
            "10 h",
            "18:00",
            "sunday",
            "monday at 12:00",
        ],
    )
    retention: Optional[str | int] = Field(
        10,
        title="日志保留方式",
        examples=[
            10,
            "1 week, 3 days",
            "2 months",
        ],
    )

    @validator("retention")
    def check_retention(cls, value: str | int) -> str | int:
        """校验日志文件保存设置

        Args:
            value (str | int): 从环境变量中获取的设置

        Returns:
            str | int: 将纯数字的字符串转换为整数
        """
        if isinstance(value, int) and value < 0:
            raise ValueError("log file retention must be a positive integer")
        if isinstance(value, str) and value.isdigit():
            return int(value)
        return value

    class Config:
        env_prefix = "LOG_FILE_"


class _IDServiceSettings(BaseSettings):
    host: Optional[str] = Field(
        "localhost",
        title="ID服务主机地址",
        examples=["localhost", "127.0.0.1"],
    )
    port: Optional[int] = Field(3306, gt=0, title="ID服务端口")

    class Config:
        env_prefix = "ID_SERVICE_"


_SettingsT = TypeVar("_SettingsT", bound="BaseSettings")


class Settings:
    __service: Optional[_ServiceSettings]
    __database: Optional[_DatabaseSettings]
    __docs: Optional[_DocsSettings]
    __log: Optional[_LogSettings]
    __id_service: Optional[_IDServiceSettings]

    __env_file_config: dict[str, Any] = {
        "_env_file": ".env",
        "_env_file_encoding": "utf-8",
    }

    def __get_settings__(self, field_name: str, _class: Type[_SettingsT]) -> _SettingsT:
        field_value: Optional[_SettingsT] = getattr(self, field_name, None)

        if field_value is None:
            field_value = _class(**self.__env_file_config)
            setattr(self, field_name, field_value)
            return field_value

        return field_value

    @property
    def service(self) -> _ServiceSettings:
        """服务设置"""
        return self.__get_settings__("__service", _ServiceSettings)

    @property
    def database(self) -> _DatabaseSettings:
        """数据库设置"""
        return self.__get_settings__("__database", _DatabaseSettings)

    @property
    def docs(self) -> _DocsSettings:
        """文档设置"""
        return self.__get_settings__("__docs", _DocsSettings)

    @property
    def log(self) -> _LogSettings:
        """日志设置"""
        return self.__get_settings__("__log", _LogSettings)

    @property
    def id_service(self) -> _IDServiceSettings:
        """ID 服务设置"""
        return self.__get_settings__("__id_service", _IDServiceSettings)

    def set_env_files_path(self, env_file_path: Path) -> None:
        """修改用于加载环境变量的文件路径

        Args:
            env_file_path (Path): 文件路径. Defaults to None.
        """

        if not env_file_path.is_file():
            raise FileNotFoundError(f"{env_file_path} is not a file.")

        if not env_file_path.exists():
            raise FileNotFoundError(f"Env file {env_file_path} not found.")

        self.__env_file_config.update({"_env_file": env_file_path})


SETTINGS = Settings()
