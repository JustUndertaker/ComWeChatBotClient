from enum import Enum

from wechatbot_client.cmd import uninstall
from wechatbot_client.grpc import GrpcManager
from wechatbot_client.grpc.model import Functions, Request
from wechatbot_client.log import logger


class Action(str, Enum):
    """
    api调用枚举，对应proto的Functions
    """

    FUNC_GET_CONTACTS = "get_contacts"
    """获取联系人"""
    FUNC_GET_DB_NAMES = "get_db_names"
    """获取数据库名称"""
    FUNC_GET_DB_TABLES = "get_db_tables"
    """获取数据库表"""
    FUNC_SEND_TXT = "send_text"
    """发送文本消息"""
    FUNC_SEND_IMG = "send_image"
    """发送图片消息"""
    FUNC_SEND_FILE = "send_file"
    """发送文件"""
    FUNC_SEND_XML = "send_xml"
    """发送xml"""
    FUNC_ACCEPT_FRIEND = "accept_friend"
    """接受好友请求"""
    FUNC_ADD_ROOM_MEMBERS = "add_room_members"
    """拉好友进群"""

    def action_to_function(self) -> Functions:
        """
        action转换为function
        """
        for func in Functions:
            if func.name == self.name:
                return func


class ApiManager:
    """
    api管理器，负责与grpc沟通调用api
    """

    grpc: GrpcManager
    """
    grpc通信管理器
    """

    def __init__(self) -> None:
        self.grpc = GrpcManager()

    def init(self) -> None:
        """
        初始化grpc
        """
        self.grpc.init()
        if not self.check_is_login():
            logger.info("<r>微信未登录，请登陆后操作</r>")
            result = self.grpc.wait_for_login()
            if not result:
                logger.info("<g>进程退出...</g>")
                self.close()
                exit(0)
        logger.info("<g>微信已登录，出发...</g>")

    def close(self) -> None:
        """
        关闭
        """
        self.grpc.close()
        uninstall("./wcf.exe")

    def connect_msg_socket(self) -> bool:
        """
        连接到接收socket
        """
        return self.grpc.connect_msg_socket()

    def get_wxid(self) -> str:
        """
        获取wxid
        """
        request = Request(func=Functions.FUNC_GET_SELF_WXID)
        result = self.grpc.request_sync(request)
        return result.string

    def check_is_login(self) -> bool:
        """
        检测是否登录
        """
        request = Request(func=Functions.FUNC_IS_LOGIN)
        result = self.grpc.request_sync(request)
        return result.status == 1
