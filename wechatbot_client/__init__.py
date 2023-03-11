import importlib

from fastapi import FastAPI

from wechatbot_client.config import Config, Env
from wechatbot_client.driver import Driver
from wechatbot_client.log import default_filter, log_init, logger
from wechatbot_client.wechat import WeChatManager

_WeChat: WeChatManager = None
"""微信管理器"""


def init() -> None:
    """
    初始化client
    """
    global _WeChat
    env = Env()
    config = Config(_common_config=env.dict())
    default_filter.level = config.log_level
    log_init(config.log_days)
    logger.info(f"Current <y><b>Env: {env.environment}</b></y>")
    logger.debug(f"Loaded <y><b>Config</b></y>: {str(config.dict())}")

    _WeChat = WeChatManager(config)
    _WeChat.init()


def run() -> None:
    """
    启动
    """
    driver = get_driver()
    driver.run()


def get_driver() -> Driver:
    """
    获取后端驱动器
    """
    wechat = get_wechat()
    return wechat.driver


def get_wechat() -> WeChatManager:
    """
    获取wechat管理器
    """
    if _WeChat is None:
        raise ValueError("wechat管理端尚未初始化...")
    return _WeChat


def get_app() -> FastAPI:
    """获取 Server App 对象。

    返回:
        Server App 对象

    异常:
        ValueError: 全局 `Driver` 对象尚未初始化 (`wechatferry_client.init` 尚未调用)
    """
    driver = get_driver()
    return driver.server_app


def load(name: str) -> None:
    """
    加载指定的模块
    """
    importlib.import_module(name)
    logger.success(f"<g>加载[{name}]成功...</g>")
