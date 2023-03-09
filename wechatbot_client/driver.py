"""
全局后端驱动
"""
import logging
from typing import Callable, Optional

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from .config import Config as BaseConfig


class Config(BaseModel):
    """配置"""

    fastapi_openapi_url: Optional[str] = None
    """`openapi.json` 地址，默认为 `None` 即关闭"""
    fastapi_docs_url: Optional[str] = None
    """`swagger` 地址，默认为 `None` 即关闭"""
    fastapi_redoc_url: Optional[str] = None
    """`redoc` 地址，默认为 `None` 即关闭"""
    fastapi_include_adapter_schema: bool = True
    """是否包含适配器路由的 schema，默认为 `True`"""
    fastapi_reload: bool = False
    """开启/关闭冷重载"""
    fastapi_reload_dirs: Optional[list[str]] = None
    """重载监控文件夹列表，默认为 uvicorn 默认值"""
    fastapi_reload_delay: Optional[float] = None
    """重载延迟，默认为 uvicorn 默认值"""
    fastapi_reload_includes: Optional[list[str]] = None
    """要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值"""
    fastapi_reload_excludes: Optional[list[str]] = None
    """不要监听的文件列表，支持 glob pattern，默认为 uvicorn 默认值"""

    class Config:
        extra = "ignore"


class Driver:
    """驱动器"""

    def __init__(self, config: BaseConfig):
        self.fastapi_config = Config.parse_obj(config)
        self.config = config
        self._server_app = FastAPI(
            openapi_url=self.fastapi_config.fastapi_openapi_url,
            docs_url=self.fastapi_config.fastapi_docs_url,
            redoc_url=self.fastapi_config.fastapi_redoc_url,
        )

    @property
    def server_app(self) -> FastAPI:
        """`FastAPI APP` 对象"""
        return self._server_app

    @property
    def logger(self) -> logging.Logger:
        """fastapi 使用的 logger"""
        return logging.getLogger("fastapi")

    def on_startup(self, func: Callable) -> Callable:
        """参考文档: [Events](https://fastapi.tiangolo.com/advanced/events/#startup-event>)"""
        return self.server_app.on_event("startup")(func)

    def on_shutdown(self, func: Callable) -> Callable:
        """参考文档: [Events](https://fastapi.tiangolo.com/advanced/events/#shutdown-event)"""
        return self.server_app.on_event("shutdown")(func)

    def run(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        *,
        app: Optional[str] = None,
        **kwargs,
    ):
        """使用 `uvicorn` 启动 FastAPI"""
        LOGGING_CONFIG = {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "default": {
                    "class": "wechatbot_client.log.LoguruHandler",
                },
            },
            "loggers": {
                "uvicorn.error": {"handlers": ["default"], "level": "INFO"},
                "uvicorn.access": {
                    "handlers": ["default"],
                    "level": "INFO",
                },
            },
        }
        uvicorn.run(
            app or self.server_app,  # type: ignore
            host=host or str(self.config.host),
            port=port or self.config.port,
            reload=self.fastapi_config.fastapi_reload,
            reload_dirs=self.fastapi_config.fastapi_reload_dirs,
            reload_delay=self.fastapi_config.fastapi_reload_delay,
            reload_includes=self.fastapi_config.fastapi_reload_includes,
            reload_excludes=self.fastapi_config.fastapi_reload_excludes,
            log_config=LOGGING_CONFIG,
            **kwargs,
        )
