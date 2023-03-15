"""
定时器模块
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from wechatbot_client.utils import logger_wrapper

log = logger_wrapper("scheduler")
scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")


def scheduler_init() -> None:
    """定时器初始化"""
    global scheduler
    if not scheduler.running:
        scheduler.start()
        log("SUCCESS", "<g>定时器模块已开启...</g>")


def scheduler_shutdown() -> None:
    """定时器关闭"""
    log("INFO", "<y>正在关闭定时器...</y>")
    if scheduler.running:
        scheduler.shutdown(wait=False)
    log("SUCCESS", "<g>定时器模块已关闭...</g>")
