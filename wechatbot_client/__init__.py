from functools import partial

from fastapi import FastAPI

from wechatbot_client.config import Config, Env
from wechatbot_client.driver import Driver
from wechatbot_client.http import router
from wechatbot_client.log import default_filter, log_init, logger
from wechatbot_client.wechat import get_wechat

_Driver: Driver = None
"""全局后端驱动器"""


def init() -> None:
    """
    初始化client
    """
    global _Driver
    env = Env()
    config = Config(_common_config=env.dict())
    default_filter.level = config.log_level
    log_init(config.log_days)
    logger.info(f"Current <y><b>Env: {env.environment}</b></y>")
    logger.debug(f"Loaded <y><b>Config</b></y>: {str(config.dict())}")

    _Driver = Driver(config)
    _WeChat = get_wechat()
    _WeChat.init(config)

    app = _Driver.server_app
    app.include_router(router)
    logger.success("<g>http api已开启...</g>")
    file_path = config.cache_path
    _Driver.on_startup(partial(_WeChat.open_recv_msg, file_path))
    _Driver.on_shutdown(_WeChat.close)


def run() -> None:
    """
    启动
    """

    _Driver.run()


def get_driver() -> Driver:
    """
    获取后端驱动器
    """
    if _Driver is None:
        raise ValueError("驱动器尚未初始化...")
    return _Driver


def get_app() -> FastAPI:
    """获取 Server App 对象。

    返回:
        Server App 对象

    异常:
        ValueError: 全局 `Driver` 对象尚未初始化 (`wechatferry_client.init` 尚未调用)
    """
    driver = get_driver()
    return driver.server_app
