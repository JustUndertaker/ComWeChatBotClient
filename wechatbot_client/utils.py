"""
工具模块，所有的工具
"""
import asyncio
import dataclasses
import inspect
import json
import re
from base64 import b64encode
from functools import partial, wraps
from typing import Any, Callable, Coroutine, ForwardRef, Optional, ParamSpec, TypeVar

from pydantic.typing import evaluate_forwardref

from wechatbot_client.log import logger
from wechatbot_client.typing import overrides

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


def get_typed_signature(call: Callable[..., Any]) -> inspect.Signature:
    """获取可调用对象签名"""
    signature = inspect.signature(call)
    globalns = getattr(call, "__globals__", {})
    typed_params = [
        inspect.Parameter(
            name=param.name,
            kind=param.kind,
            default=param.default,
            annotation=get_typed_annotation(param, globalns),
        )
        for param in signature.parameters.values()
    ]
    return inspect.Signature(typed_params)


def get_typed_annotation(param: inspect.Parameter, globalns: dict[str, Any]) -> Any:
    """获取参数的类型注解"""
    annotation = param.annotation
    if isinstance(annotation, str):
        annotation = ForwardRef(annotation)
        try:
            annotation = evaluate_forwardref(annotation, globalns, globalns)
        except Exception as e:
            logger.opt(colors=True, exception=e).warning(
                f'Unknown ForwardRef["{param.annotation}"] for parameter {param.name}'
            )
            return inspect.Parameter.empty
    return annotation


def logger_wrapper(logger_name: str):
    """用于打印 adapter 的日志。

    参数:
        logger_name: adapter 的名称

    返回:
        日志记录函数

            - level: 日志等级
            - message: 日志信息
            - exception: 异常信息
    """

    def log(level: str, message: str, exception: Optional[Exception] = None):
        logger.opt(colors=True, exception=exception).log(
            level, f"<m>{escape_tag(logger_name)}</m> | {message}"
        )

    return log


class DataclassEncoder(json.JSONEncoder):
    """在JSON序列化 `Message` (List[Dataclass]) 时使用的 `JSONEncoder`"""

    @overrides(json.JSONEncoder)
    def default(self, o):
        if isinstance(o, bytes):
            return b64encode(o).decode()
        if dataclasses.is_dataclass(o):
            return {f.name: getattr(o, f.name) for f in dataclasses.fields(o)}
        return super().default(o)
