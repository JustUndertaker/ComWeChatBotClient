"""
配置模块
"""
import os
from enum import Enum
from ipaddress import IPv4Address
from typing import TYPE_CHECKING, Any, Mapping, Optional, Tuple, Union

from pydantic import AnyUrl, BaseSettings, Extra, Field, IPvAnyAddress
from pydantic.env_settings import (
    DotenvType,
    EnvSettingsSource,
    InitSettingsSource,
    SettingsError,
    SettingsSourceCallable,
)
from pydantic.utils import deep_update

from .log import logger


class CustomEnvSettings(EnvSettingsSource):
    def __call__(self, settings: BaseSettings) -> dict[str, Any]:
        """
        Build environment variables suitable for passing to the Model.
        """
        d: dict[str, Any] = {}

        if settings.__config__.case_sensitive:
            env_vars: Mapping[str, Optional[str]] = os.environ  # pragma: no cover
        else:
            env_vars = {k.lower(): v for k, v in os.environ.items()}

        env_file_vars = self._read_env_files(settings.__config__.case_sensitive)
        env_vars = {**env_file_vars, **env_vars}

        for field in settings.__fields__.values():
            env_val: Optional[str] = None
            for env_name in field.field_info.extra["env_names"]:
                env_val = env_vars.get(env_name)
                if env_name in env_file_vars:
                    del env_file_vars[env_name]
                if env_val is not None:
                    break

            is_complex, allow_parse_failure = self.field_is_complex(field)
            if is_complex:
                if env_val is None:
                    if env_val_built := self.explode_env_vars(field, env_vars):
                        d[field.alias] = env_val_built
                else:
                    # field is complex and there's a value, decode that as JSON, then add explode_env_vars
                    try:
                        env_val = settings.__config__.parse_env_var(field.name, env_val)
                    except ValueError as e:
                        if not allow_parse_failure:
                            raise SettingsError(
                                f'error parsing env var "{env_name}"'  # type: ignore
                            ) from e

                    if isinstance(env_val, dict):
                        d[field.alias] = deep_update(
                            env_val, self.explode_env_vars(field, env_vars)
                        )
                    else:
                        d[field.alias] = env_val
            elif env_val is not None:
                # simplest case, field is not complex, we only need to add the value if it was found
                d[field.alias] = env_val

        # remain user custom config
        for env_name in env_file_vars:
            env_val = env_vars[env_name]
            if env_val and (val_striped := env_val.strip()):
                # there's a value, decode that as JSON
                try:
                    env_val = settings.__config__.parse_env_var(env_name, val_striped)
                except ValueError:
                    logger.trace(
                        "Error while parsing JSON for "
                        f"{env_name!r}={val_striped!r}. "
                        "Assumed as string."
                    )

            # explode value when it's a nested dict
            env_name, *nested_keys = env_name.split(self.env_nested_delimiter)
            if nested_keys and (env_name not in d or isinstance(d[env_name], dict)):
                result = {}
                *keys, last_key = nested_keys
                _tmp = result
                for key in keys:
                    _tmp = _tmp.setdefault(key, {})
                _tmp[last_key] = env_val
                d[env_name] = deep_update(d.get(env_name, {}), result)
            elif not nested_keys:
                d[env_name] = env_val

        return d


class BaseConfig(BaseSettings):
    if TYPE_CHECKING:
        # dummy getattr for pylance checking, actually not used
        def __getattr__(self, name: str) -> Any:  # pragma: no cover
            return self.__dict__.get(name)

    class Config:
        extra = Extra.allow
        env_nested_delimiter = "__"

        @classmethod
        def customise_sources(
            cls,
            init_settings: InitSettingsSource,
            env_settings: EnvSettingsSource,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            common_config = init_settings.init_kwargs.pop("_common_config", {})
            return (
                init_settings,
                CustomEnvSettings(
                    env_settings.env_file,
                    env_settings.env_file_encoding,
                    env_settings.env_nested_delimiter,
                    env_settings.env_prefix_len,
                ),
                InitSettingsSource(common_config),
                file_secret_settings,
            )


class Env(BaseConfig):
    """运行环境配置。大小写不敏感。

    将会从 `环境变量` > `.env 环境配置文件` 的优先级读取环境信息。
    """

    environment: str = "prod"
    """当前环境名。

    将从 `.env.{environment}` 文件中加载配置。
    """

    class Config:
        env_file = ".env"


class WebsocketType(str, Enum):
    """websocket连接枚举"""

    Unable = "Unable"
    """不开启ws"""
    Forward = "Forward"
    """正向ws"""
    Backward = "Backward"
    """反向ws"""


class WSUrl(AnyUrl):
    """ws或wss url"""

    allow_schemes = {"ws", "wss"}


class Config(BaseConfig):
    """主要配置"""

    _env_file: DotenvType = ".env", ".env.prod"
    host: IPvAnyAddress = IPv4Address("127.0.0.1")
    """服务host"""
    port: int = Field(default=8080, ge=1, le=65535)
    """服务端口"""
    access_token: str = ""
    """访问令牌"""
    heartbeat_enabled: bool = False
    """是否开启心跳"""
    heartbeat_interval: int = 5000
    """心跳间隔"""
    enable_http_api: bool = False
    """是否开启http api"""
    event_enabled: bool = False
    """是否启用 get_latest_events 元动作"""
    event_buffer_size: int = 0
    """事件缓冲区大小，超过该大小将会丢弃最旧的事件，0 表示不限大小"""
    enable_http_webhook: bool = False
    """是否启用http webhook"""
    webhook_url: set[AnyUrl] = Field(default_factory=set)
    """webhook 上报地址"""
    webhook_timeout: int = 5000
    """上报请求超时时间，单位：毫秒，0 表示不超时"""
    websocekt_type: WebsocketType = WebsocketType.Backward
    """websocket连接方式"""
    websocket_url: set[WSUrl] = Field(default_factory=set)
    """反向 WebSocket 连接地址"""
    websocket_buffer_size: int = 4
    """反向 WebSocket 的缓冲区大小，单位(Mb)"""
    reconnect_interval: int = 5000
    """反向 WebSocket 重连间隔"""
    log_level: Union[int, str] = "INFO"
    """默认日志等级"""
    log_days: int = 10
    """日志保存天数"""
    cache_days: int = 3
    """文件缓存天数"""

    class Config:
        extra = "allow"
