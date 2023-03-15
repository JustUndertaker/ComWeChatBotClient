"""
启动行为管理，将各类业务剥离开
"""
import asyncio
import time
from functools import partial
from uuid import uuid4

from comtypes.client import PumpEvents

from wechatbot_client import get_driver, get_wechat
from wechatbot_client.config import Config, WebsocketType
from wechatbot_client.consts import FILE_CACHE
from wechatbot_client.driver import URL, HTTPServerSetup, WebSocketServerSetup
from wechatbot_client.file_manager import database_close, database_init
from wechatbot_client.log import logger
from wechatbot_client.onebot12 import HeartbeatMetaEvent
from wechatbot_client.scheduler import scheduler, scheduler_init, scheduler_shutdown
from wechatbot_client.test import router

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
        scheduler.add_job(
            func=partial(heartbeat_event, config.heartbeat_interval),
            trigger="interval",
            seconds=int(config.heartbeat_interval / 1000),
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
    logger.debug("开启测试http路由")
    driver._server_app.include_router(router)


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
    # 关闭所有ws连接
    for ws in driver.connects.values():
        await ws.close()
    wechat.close()


async def pump_event() -> None:
    """接收event循环"""
    while True:
        try:
            await asyncio.sleep(0)
            PumpEvents(0.01)
        except KeyboardInterrupt:
            logger.info("<g>事件接收已关闭，再使用 'ctrl + c' 结束进程...</g>")
            return


async def heartbeat_event(interval: int) -> None:
    """
    心跳事件
    """
    event_id = str(uuid4())
    event = HeartbeatMetaEvent(id=event_id, time=time.time(), interval=interval)
    await wechat.handle_event(event)
