from typing import Optional

from loguru import logger

from app.util.env import LOG_FILE_ROTATION as ROTATION
from app.util.env import LOG_FILE_RETENTION as RETENTION


class Log:
    __log_format: dict
    __handler_id: Optional[int] = 0

    def __init__(self, **kwargs):
        self.__log_format = kwargs

    def start_logging(self) -> None:
        """开始记录日志"""
        self.__handler_id = logger.add(**self.__log_format)

    def stop_logging(self) -> None:
        """停止记录日志"""
        logger.info("Shutting down...")
        if self.__handler_id is not None:
            logger.remove(self.__handler_id)
            self.__handler_id = None


LOG = Log(
    sink="logs/log.log",
    enqueue=True,
    rotation=ROTATION,
    retention=int(RETENTION) if RETENTION.isdigit() else RETENTION,
    compression="tar.gz",
)
