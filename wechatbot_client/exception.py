"""
异常模块，这里定义所有异常
"""


from typing import Optional


class BaseException(Exception):
    """异常基类"""

    def __str__(self) -> str:
        return self.__repr__()


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
