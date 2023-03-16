"""
异常模块，这里定义所有异常
"""


from typing import Optional


class BaseException(Exception):
    """异常基类"""

    def __str__(self) -> str:
        return self.__repr__()


class MessageException(BaseException):
    """消息异常"""

    ...


class NoThisUserInGroup(MessageException):
    """群聊中查无此人"""

    group_id: str
    user_id: str

    def __init__(self, group_id: str, user_id: str) -> None:
        self.group_id = group_id
        self.user_id = user_id

    def __repr__(self) -> str:
        return f"在[{self.group_id}]查无此人:{self.user_id}"


class FileNotFound(MessageException):
    """文件未找到"""

    file_id: str

    def __init__(self, file_id: str) -> None:
        self.file_id = file_id

    def __repr__(self) -> str:
        return f"未找到文件:{self.file_id}"


class WebSocketClosed(BaseException):
    """WebSocket 连接已关闭"""

    def __init__(self, code: int, reason: Optional[str] = None) -> None:
        self.code = code
        self.reason = reason

    def __repr__(self) -> str:
        return (
            f"WebSocketClosed(code={self.code}"
            + (f", reason={self.reason!r}" if self.reason else "")
            + ")"
        )
