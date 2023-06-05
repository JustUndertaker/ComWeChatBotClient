"""
启动行为管理，将各类业务剥离开
"""
import asyncio
import time
from functools import partial
from signal import SIGINT, raise_signal
from uuid import uuid4

from comtypes.client import PumpEvents

from wechatbot_client import get_driver, get_wechat
from wechatbot_client.action_manager import router
from wechatbot_client.config import Config, WebsocketType
from wechatbot_client.consts import FILE_CACHE
from wechatbot_client.driver import URL, HTTPServerSetup, WebSocketServerSetup
from wechatbot_client.file_manager import database_close, database_init
from wechatbot_client.log import logger
from wechatbot_client.onebot12 import HeartbeatMetaEvent
from wechatbot_client.scheduler import scheduler, scheduler_init, scheduler_shutdown

driver = get_driver()
wechat = get_wechat()
pump_event_task: asyncio.Task = None


@driver.on_startup
async def start_up() -> None:
    """
    启动行为管理
    """
    global pump_event_task
    config: Config = wechat.config
    # 开启定时器
    scheduler_init()
    # 开启心跳事件
    if config.heartbeat_enabled:
        logger.debug(f"开启心跳事件，间隔 {config.heartbeat_interval} ms")
        scheduler.add_job(
            func=partial(heartbeat_event, config.heartbeat_interval),
            trigger="interval",
            seconds=int(config.heartbeat_interval / 1000),
        )
    # 开启自动清理缓存
    if config.cache_days > 0:
        logger.debug(f"开启自动清理缓存，间隔 {config.cache_days} 天")
        scheduler.add_job(
            func=partial(clean_filecache, config.cache_days),
            trigger="cron",
            hour=0,
            minute=0,
            second=0,
        )
    # 开启数据库
    await database_init()
    # 注册消息事件
    wechat.open_recv_msg(f"./{FILE_CACHE}")
    # 开始监听event
    pump_event_task = asyncio.create_task(pump_event())
    # 开启http路由
    if config.enable_http_api:
        wechat.setup_http_server(
            HTTPServerSetup(URL("/"), "POST", "onebot", wechat.handle_http)
        )
    # 开启ws连接任务
    if config.websocekt_type == WebsocketType.Forward:
        # 正向ws，建立监听
        wechat.setup_websocket_server(
            WebSocketServerSetup(URL("/"), "onebot", wechat.handle_ws)
        )
    elif config.websocekt_type == WebsocketType.Backward:
        # 反向ws，连接应用端
        await wechat.start_backward()
    # 添加get_file路由
    driver.server_app.include_router(router)


@driver.on_shutdown
async def shutdown() -> None:
    """
    关闭行为管理
    """
    # 关闭定时器
    scheduler_shutdown()
    # 关闭数据库
    await database_close()
    if pump_event_task:
        if not pump_event_task.done():
            pump_event_task.cancel()
    await wechat.stop_backward()
    wechat.close()


async def pump_event() -> None:
    """接收event循环"""
    while True:
        try:
            await asyncio.sleep(0)
            PumpEvents(0.01)
        except KeyboardInterrupt:
            raise_signal(SIGINT)
            return


async def heartbeat_event(interval: int) -> None:
    """
    心跳事件
    """
    event_id = str(uuid4())
    event = HeartbeatMetaEvent(
        id=event_id,
        time=time.time(),
        interval=interval,
    )
    await wechat.handle_event(event)


async def clean_filecache(days: int) -> None:
    """
    自动清理缓存
    """
    logger.info("<g>开始清理文件缓存任务...</g>")
    nums = await wechat.file_manager.clean_cache(days)
    logger.success(f"<g>清理缓存完成，共清理 {nums} 个文件...</g>")
