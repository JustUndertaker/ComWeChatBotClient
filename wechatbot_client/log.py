"""
日志模块
"""
import logging
import sys
from pathlib import Path
from typing import Union

from loguru._logger import Core, Logger

from wechatbot_client.consts import LOG_PATH

logger = Logger(
    core=Core(),
    exception=None,
    depth=0,
    record=False,
    lazy=False,
    colors=True,
    raw=False,
    capture=True,
    patcher=None,
    extra={},
)
"""logger对象"""


class Filter:
    """过滤器类"""

    def __init__(self) -> None:
        self.level: Union[int, str] = "INFO"

    def __call__(self, record):
        module_name: str = record["name"]
        record["name"] = module_name.split(".")[0]
        levelno = (
            logger.level(self.level).no if isinstance(self.level, str) else self.level
        )
        return record["level"].no >= levelno


default_format: str = (
    "<g>{time:MM-DD HH:mm:ss}</g> "
    "[<lvl>{level:^7}</lvl>] "
    "<c><u>{name:16}</u></c> | "
    # "<c>{function}:{line}</c>| "
    "{message}"
)
"""默认日志格式"""


class LoguruHandler(logging.Handler):  # pragma: no cover
    def emit(self, record) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


default_filter = Filter()
logger_id = logger.add(
    sys.stdout,
    level=0,
    diagnose=False,
    filter=default_filter,
    format=default_format,
)


def log_init(log_days: int) -> None:
    """日志初始化"""
    cwd = Path(".") / LOG_PATH
    info_path = cwd / "info"
    debug_path = cwd / "debug"
    error_path = cwd / "error"
    info_path.mkdir(parents=True, exist_ok=True)
    debug_path.mkdir(parents=True, exist_ok=True)
    error_path.mkdir(parents=True, exist_ok=True)
    # 日志文件记录格式
    file_format = (
        "<g>{time:MM-DD HH:mm:ss}</g> "
        "[<lvl>{level}</lvl>] "
        "<c><u>{name}</u></c> | "
        "{message}"
    )

    # 错误日志文件记录格式
    error_format = (
        "<g>{time:MM-DD HH:mm:ss}</g> "
        "[<lvl>{level}</lvl>] "
        "[<c><u>{name}</u></c>] | "
        "<c>{function}:{line}</c>| "
        "{message}"
    )
    logger.add(
        f"./{LOG_PATH}/info/" + "{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention=f"{log_days} days",
        level="INFO",
        format=file_format,
        filter=default_filter,
        encoding="utf-8",
    )
    logger.add(
        f"./{LOG_PATH}/debug/" + "{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention=f"{log_days} days",
        level="DEBUG",
        format=file_format,
        filter=default_filter,
        encoding="utf-8",
    )
    logger.add(
        f"./{LOG_PATH}/error/" + "{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention=f"{log_days} days",
        level="ERROR",
        format=error_format,
        filter=default_filter,
        encoding="utf-8",
    )
