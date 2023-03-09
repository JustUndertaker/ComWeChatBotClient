"""
微信客户端抽象，整合各种请求需求
"""
from .action_check import gen_action_dict
from .wechat import WeChatManager as WeChatManager

_WeChat = WeChatManager()
"""微信管理器"""


def get_wechat() -> WeChatManager:
    """
    获取wechat管理器
    """
    if _WeChat is None:
        raise ValueError("wechat管理端尚未初始化...")
    return _WeChat
