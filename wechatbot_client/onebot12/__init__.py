"""
onebot12的消息与事件
"""
from .event import *
from .message import Message as Message
from .message import MessageSegment as MessageSegment

__all__ = [
    "Message",
    "MessageSegment",
    "Event",
    "PrivateMessageEvent",
    "GroupMessageEvent",
    "FriendIncreaseEvent",
    "FriendDecreaseEvent",
    "PrivateMessageDeleteEvent",
    "GroupMemberIncreaseEvent",
    "GroupMemberDecreaseEvent",
    "GroupAdminSetEvent",
    "GroupAdminUnsetEvent",
    "GroupMessageDeleteEvent",
    "GetPrivateFileNotice",
    "GetGroupFileNotice",
    "HeartbeatMetaEvent",
]
