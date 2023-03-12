"""
启动行为管理，将各类业务剥离开
"""
import asyncio

from comtypes.client import PumpEvents

from wechatbot_client import get_driver, get_wechat
from wechatbot_client.config import Config, WebsocketType
from wechatbot_client.driver import URL, HTTPServerSetup, WebSocketServerSetup
from wechatbot_client.log import logger

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
    # 注册消息事件
    wechat.open_recv_msg(config.cache_path)
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


@driver.on_shutdown
async def shutdown() -> None:
    """
    关闭行为管理
    """
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
            logger.info("<g>事件接收已关闭，再使用 'ctrl + c' 结束进程...</g>")
            return
