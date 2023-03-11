"""
启动行为管理，将各类业务剥离开
"""
import asyncio

from comtypes.client import PumpEvents

from wechatbot_client import get_driver
from wechatbot_client.com.http import router
from wechatbot_client.log import logger

driver = get_driver()


@driver.on_startup
async def start_up() -> None:
    """
    启动行为管理
    """
    # 开始监听event
    asyncio.create_task(pump_event())
    logger.success("<g>监听消息任务已开启...</g>")
    driver.server_app.include_router(router)
    logger.success("<g>http api已开启...</g>")


async def pump_event() -> None:
    """接收event循环"""
    while True:
        try:
            await asyncio.sleep(0)
            PumpEvents(0.01)
        except KeyboardInterrupt:
            logger.info("<g>事件接收已关闭，再使用 'ctrl + c' 结束进程...</g>")
            await driver.server_app.router.shutdown()
            return
