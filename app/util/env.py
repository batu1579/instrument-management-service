from os import getenv
from typing import TypeVar

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(".env"))

DefaultValue = TypeVar("DefaultValue", str, None)


def _get_env_var(key: str, default: DefaultValue = None) -> str | DefaultValue:
    """将 .env 文件中不填写值时被识别为空字符串的情况替换为默认值

    Args:
        key (str): 环境变量键名
        default (Optional[str]): 未设置值时使用的默认值. 默认为 None.

    Returns:
        str | None: 返回获取到的环境变量，如果环境变量不存在则返回设置的默认值，若未设置默认值则返回 None.
    """
    env_var = getenv(key)

    if env_var is None or env_var == "":
        env_var = default

    return env_var


HOST = _get_env_var("HOST", "localhost")
PORT = int(_get_env_var("PORT", "8081"))

USE_HTTPS_ONLY = _get_env_var("USE_HTTPS_ONLY") == "True"

KEYFILE = _get_env_var("KEYFILE")
CERTFILE = _get_env_var("CERTFILE")

TITLE = _get_env_var("TITLE", "FastAPI")

ORIGINS = _get_env_var("ORIGINS", "http://localhost")

GZIP_MIN_SIZE = int(_get_env_var("GZIP_MIN_SIZE", "500"))

LOG_FILE_ROTATION = _get_env_var("LOG_FILE_SIZE", "200 MB")
LOG_FILE_RETENTION = _get_env_var("LOG_FILE_RETENTION", "10")

DOCS_URL = _get_env_var("DOCS_URL", "/docs")
REDOCS_URL = _get_env_var("REDOCS_URL", "/redocs")

DB_HOST = _get_env_var("DB_HOST", "localhost")
DB_PORT = int(_get_env_var("DB_PORT", "3306"))

DB_USER = _get_env_var("DB_USER")
DB_PASSWORD = _get_env_var("DB_PASSWORD")

DB_NAME = _get_env_var("DB_NAME")

ID_SERVICE_HOST = _get_env_var("ID_SERVICE_HOST", "localhost")
ID_SERVICE_PORT = int(_get_env_var("ID_SERVICE_PORT", "8910"))
