"""
用来检测action参数的模块
"""

from inspect import Parameter
from typing import Any, Callable, Type

from pydantic import BaseConfig, BaseModel, Extra, ValidationError, create_model

from wechatbot_client.log import logger
from wechatbot_client.utils import get_typed_signature

from .action import ActionRequest

ACTION_DICT: dict[str, Type[BaseModel]] = {}
"""action模型字典"""


class ModelConfig(BaseConfig):
    """action模型config"""

    extra = Extra.forbid


def check_action_params(request: ActionRequest) -> None:
    """
    说明:
        检测action的参数合法性，会检测`action`是否存在，同时param类型是否符合

    参数:
        * `request`：action请求

    返回:
        * `None`: 检测通过

    错误:
        * `TypeError`: 未实现action
        * `ValueError`: 参数错误
    """
    if request.params is None:
        request.params = {}

    action_model = ACTION_DICT.get(request.action)
    if action_model is None:
        logger.error(f"<r>未实现的action:{request.action}</r>")
        raise TypeError(f"未实现的action:{request.action}")

    try:
        action_model.parse_obj(request.params)
    except ValidationError as e:
        logger.error(f"<r>action参数错误:{e}</r>")
        raise ValueError("请求参数错误...")
    return


def add_action(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    说明:
        使用此装饰器表示将此函数加入action字典中，会生成验证模型，注意参数的类型标注
    """

    global ACTION_DICT
    signature = get_typed_signature(func)
    field = {}
    for parameter in signature.parameters.values():
        name = parameter.name
        annotation = parameter.annotation
        default = parameter.default
        if name != "self":
            if default == Parameter.empty:
                field[name] = (annotation, ...)
            else:
                field[name] = (annotation, default)
    action_type = create_model(func.__name__, __config__=ModelConfig, **field)
    ACTION_DICT[func.__name__] = action_type
    return func
