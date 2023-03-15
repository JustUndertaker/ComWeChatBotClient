"""
定时器模块
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .log import logger

scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")


def scheduler_init() -> None:
    """定时器初始化"""
    global scheduler
    if not scheduler.running:
        scheduler.start()
        logger.success("<m>scheduler</m> - <g>定时器模块已开启...</g>")


def scheduler_shutdown() -> None:
    """定时器关闭"""
    logger.info("<m>scheduler</m> - 正在关闭定时器...")
    if scheduler.running:
        scheduler.shutdown(wait=False)
    logger.success("<m>scheduler</m> - <g>定时器关闭成功...</g>")
