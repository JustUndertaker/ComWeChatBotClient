"""
工具模块
"""
import asyncio
import re
from functools import partial, wraps
from typing import Callable, Coroutine, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def escape_tag(s: str) -> str:
    """用于记录带颜色日志时转义 `<tag>` 类型特殊标签

    参考: [loguru color 标签](https://loguru.readthedocs.io/en/stable/api/logger.html#color)

    参数:
        s: 需要转义的字符串
    """
    return re.sub(r"</?((?:[fb]g\s)?[^<>\s]*)>", r"\\\g<0>", s)


def run_sync(call: Callable[P, R]) -> Callable[P, Coroutine[None, None, R]]:
    """一个用于包装 sync function 为 async function 的装饰器

    参数:
        call: 被装饰的同步函数
    """

    @wraps(call)
    async def _wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        loop = asyncio.get_running_loop()
        pfunc = partial(call, *args, **kwargs)
        result = await loop.run_in_executor(None, pfunc)
        return result

    return _wrapper
