"""
消息tpye分类
"""
from enum import IntEnum


class WxType(IntEnum):
    """
    微信消息type
    """

    TEXT_MSG = 1
    """文本消息"""
    IMAGE_MSG = 3
    """图片消息"""
    VOICE_MSG = 34
    """语音消息"""
    FRIEND_REQUEST = 37
    """加好友请求"""
    CARD_MSG = 42
    """名片消息"""
    VIDEO_MSG = 43
    """视频消息"""
    EMOJI_MSG = 47
    """表情消息"""
    LOCATION_MSG = 48
    """位置消息"""
    APP_MSG = 49
    """应用消息"""
    CREATE_ROOM = 51
    """创建房间"""
    SYSTEM_MSG = 10000
    """个人系统消息"""
    GROUP_SYS_MSG = 10002
    """群系统消息"""


class AppType(IntEnum):
    """
    App消息类型
    """

    LINK_MSG = 5
    """链接消息"""
    FILE_NOTICE = 6
    """文件消息，包含提示和下载完成"""
    QUOTE = 57
    """引用消息"""
    APP = 33
    """小程序"""
    GROUP_ANNOUNCEMENT = 87
    """群公告"""
    TRANSFER = 2000
    """转账"""
