from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .type import WxType


class Message(BaseModel):
    """接收的消息"""

    extrainfo: str
    """额外信息"""
    filepath: Optional[str]
    """文件路径"""
    isSendByPhone: Optional[bool]
    """是否为手机发送，自己手动操作机器人发送时有效"""
    isSendMsg: bool
    """是否为自身发送"""
    message: str
    """消息内容"""
    msgid: int
    """消息id"""
    pid: int
    """进程pid"""
    self: str
    """自身id"""
    sender: str
    """发送方id"""
    sign: str
    """sign值"""
    thumb_path: str
    """缩略图位置"""
    time: datetime
    """发送时间"""
    timestamp: int
    """时间戳"""
    type: WxType
    """消息类型"""
    wxid: str
    """wxid"""
