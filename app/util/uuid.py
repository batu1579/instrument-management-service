from json import dumps

from loguru import logger

from snowflake import client

from app.util.env import ID_SERVICE_HOST, ID_SERVICE_PORT


def init_snowflake_client() -> None:
    """初始化 ID 服务客户端"""
    client.setup(ID_SERVICE_HOST, ID_SERVICE_PORT)

    status = dumps(client.get_stats(), indent=4)
    logger.info(f"id service status: {status}")
