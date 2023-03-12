from typing import Callable

from wechatbot_client.action_manager import ActionManager
from wechatbot_client.config import Config
from wechatbot_client.log import logger

from .adapter import Adapter


class WeChatManager(Adapter):
    """
    微信客户端行为管理
    """

    action_manager: ActionManager
    """api管理模块"""
    self_id: str
    """自身微信id"""

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.action_manager = ActionManager()
        self.self_id = None

    def init(self) -> None:
        """
        初始化wechat管理端
        """
        self.action_manager.init()

        logger.debug("<y>开始获取wxid...</y>")
        self.self_id = self.action_manager.get_wxid()
        logger.debug("<g>微信id获取成功...</g>")
        logger.info("<g>初始化完成，启动uvicorn...</g>")

    def open_recv_msg(self, file_path: str) -> None:
        """
        开始接收消息
        """
        self.action_manager.open_recv_msg(file_path)

    def close(self) -> None:
        """
        管理微信管理模块
        """
        self.action_manager.close()

    def register_message_handler(self, func: Callable[[str], None]) -> None:
        """
        注册一个消息处理器
        """
        self.action_manager.register_message_handler(func)
