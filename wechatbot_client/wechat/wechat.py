from typing import Callable

from wechatbot_client.config import Config
from wechatbot_client.log import logger

from .adapter import Adapter
from .api_manager import ApiManager


class WeChatManager(Adapter):
    """
    微信客户端行为管理
    """

    api_manager: ApiManager
    """api管理模块"""
    self_id: str
    """自身微信id"""

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.api_manager = ApiManager()
        self.self_id = None

    def init(self) -> None:
        """
        初始化wechat管理端
        """
        self.api_manager.init()

        logger.debug("<y>开始获取wxid...</y>")
        self.self_id = self.api_manager.get_wxid()
        logger.debug("<g>微信id获取成功...</g>")
        logger.info("<g>初始化完成，启动uvicorn...</g>")

    def open_recv_msg(self, file_path: str) -> None:
        """
        开始接收消息
        """
        self.api_manager.open_recv_msg(file_path)

    def close(self) -> None:
        """
        管理微信管理模块
        """
        self.api_manager.close()

    def register_message_handler(self, func: Callable[[str], None]) -> None:
        """
        注册一个消息处理器
        """
        self.api_manager.register_message_handler(func)

    async def handle_http_request(self)
