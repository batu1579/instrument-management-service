from typing import Optional

from loguru import logger

from app.util.env import SETTINGS


class Log:
    __log_config: dict
    __handler_id: Optional[int] = 0

    def __init__(self, **kwargs):
        self.__log_config = kwargs

    def start_logging(self) -> None:
        """开始记录日志"""
        self.__handler_id = logger.add(**self.__log_config)

    def stop_logging(self) -> None:
        """停止记录日志"""
        logger.info("Shutting down...")
        if self.__handler_id is not None:
            logger.remove(self.__handler_id)
            self.__handler_id = None


LOG = Log(
    sink="logs/log.log",
    enqueue=True,
    rotation=SETTINGS.log.rotation,
    retention=SETTINGS.log.retention,
    compression="tar.gz",
)
