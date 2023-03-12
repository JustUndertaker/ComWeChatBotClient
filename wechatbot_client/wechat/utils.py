from typing import Optional, TypeVar

T = TypeVar("T")


def get_auth_bearer(access_token: Optional[str] = None) -> Optional[str]:
    if not access_token:
        return None
    scheme, _, param = access_token.partition(" ")
    return param if scheme.lower() in ["bearer", "token"] else None


def flattened_to_nested(data: T) -> T:
    """将扁平键值转为嵌套字典。"""
    if isinstance(data, dict):
        pairs = [
            (
                key.split(".") if isinstance(key, str) else key,
                flattened_to_nested(value),
            )
            for key, value in data.items()
        ]
        result = {}
        for key_list, value in pairs:
            target = result
            for key in key_list[:-1]:
                target = target.setdefault(key, {})
            target[key_list[-1]] = value
        return result  # type: ignore
    elif isinstance(data, list):
        return [flattened_to_nested(item) for item in data]  # type: ignore
    return data
