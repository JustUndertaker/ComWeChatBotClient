from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple

from tortoise import Tortoise, fields
from tortoise.models import Model

from wechatbot_client.consts import DATABASE_PATH
from wechatbot_client.log import logger


class FileCache(Model):
    """文件缓存表"""

    id = fields.IntField(pk=True, generated=True)
    file_id = fields.CharField(max_length=255)
    """文件id"""
    create_time = fields.DatetimeField()
    """创建时间"""
    file_name = fields.CharField(max_length=255)
    """文件名"""
    file_path = fields.CharField(max_length=255)
    """文件路径"""
    file_temp = fields.BooleanField()
    """是否为临时文件"""

    class Meta:
        table = "file_cache"
        table_description = "文件缓存"

    @classmethod
    async def create_file_cache(
        cls, file_id: str, file_path: str, file_name: str, file_temp: bool = True
    ) -> bool:
        """
        说明:
            创建一个文件缓存

        参数:
            * `file_id`: 文件名
            * `file_path`: 文件路径
            * `file_name`: 文件名
            * `file_temp`: 是否为临时文件

        返回:
            * `bool`: 缓存是否成功
        """
        time = datetime.now()
        await cls.create(
            file_id=file_id,
            file_path=file_path,
            file_name=file_name,
            create_time=time,
            file_temp=file_temp,
        )
        return True

    @classmethod
    async def get_file(cls, file_id: str) -> Optional[Tuple[str, str]]:
        """
        说明:
            根据id查找文件名

        参数:
            * `file_id`: 文件id

        返回:
            * `str | None`: 找到的文件路径
            * `str`: 文件名
        """
        model = await cls.filter(file_id=file_id).first()
        if model:
            return model.file_path, model.file_name
        return None

    @classmethod
    async def clean_file(cls, days: int = 3) -> list[str]:
        """
        说明:
            清理超过`days`天的数据库缓存

        参数:
            * `days`: 天数
        """
        time = datetime.now() - timedelta(days=days)
        files = await cls.filter(create_time__lte=time)
        file_paths = []
        for file in files:
            if file.file_temp:
                file_paths.append(file.file_path)
            await file.delete()
        return file_paths

    @classmethod
    async def reset(cls) -> None:
        """
        重置数据库，将所有记录删除
        """
        await cls.all().delete()


async def database_init() -> None:
    """
    数据库初始化
    """
    logger.debug("<y>正在注册数据库...</y>")
    Path(f"./{DATABASE_PATH}").mkdir(exist_ok=True)
    database_path = f"./{DATABASE_PATH}/data.db"
    db_url = f"sqlite://{database_path}"
    # 这里填要加载的表
    models = [
        "wechatbot_client.file_manager.model",
    ]
    modules = {"models": models}
    await Tortoise.init(db_url=db_url, modules=modules)
    await Tortoise.generate_schemas()
    logger.info("<g>数据库初始化成功...</g>")


async def database_close() -> None:
    """
    关闭数据库
    """
    await Tortoise.close_connections()
