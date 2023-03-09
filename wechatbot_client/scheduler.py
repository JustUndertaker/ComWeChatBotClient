"""
定时器模块
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .config import Config
from .log import logger

scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")


def scheduler_init(config: Config) -> None:
    """定时器初始化"""
    global scheduler
    if not scheduler.running:
        scheduler.start()
        # scheduler.add_job(
        #     partial(scheduler_job, config), trigger="cron", hour=0, minute=0
        # )
        # scheduler.add_job(
        #     partial(scheduler_image_job, config), trigger="cron", hour=0, minute=0
        # )
        logger.success("<m>scheduler</m> - <g>定时器模块已开启...</g>")


def scheduler_shutdown() -> None:
    """定时器关闭"""
    logger.info("<m>scheduler</m> - 正在关闭定时器...")
    if scheduler.running:
        scheduler.shutdown(wait=False)
    logger.success("<m>scheduler</m> - <g>定时器关闭成功...</g>")
