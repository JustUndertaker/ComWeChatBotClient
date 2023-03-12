from datetime import datetime, timedelta
from typing import Optional

from tortoise import fields
from tortoise.models import Model


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
    cache_flag = fields.BooleanField()
    """flag，是否为要清理的文件"""

    class Meta:
        table = "file_cache"
        table_description = "文件缓存"

    @classmethod
    async def create_file_cache(
        cls, file_id: str, file_path: str, file_name: str, flag: bool = True
    ) -> bool:
        """
        说明:
            创建一个文件缓存

        参数:
            * `file_id`: 文件名
            * `file_path`: 文件路径
            * `file_name`: 文件名
            * `flag`: 清理标记，为`False`的文件在清理时不会返回`path`

        返回:
            * `bool`: 缓存是否成功
        """
        time = datetime.now()
        await cls.create(
            file_id=file_id,
            file_path=file_path,
            file_name=file_name,
            create_time=time,
            cache_flag=flag,
        )
        return True

    @classmethod
    async def get_file(cls, file_id: str) -> Optional[str]:
        """
        说明:
            根据id查找文件名

        参数:
            * `file_id`: 文件id

        返回:
            * `str | None`: 找到的文件路径
        """
        model = await cls.filter(file_id=file_id).first()
        if model:
            return model.file_path
        return None

    @classmethod
    async def clean_file(cls, days: int = 3) -> list[str]:
        """
        说明:
            清理超过`days`天的缓存

        参数:
            * `days`: 天数

        返回:
            * `list[str]`: 被清理的文件路径列表
        """
        time = datetime.now() - timedelta(days=days)
        model = await cls.filter(create_time__lte=time)
        data = []
        for one in model:
            if one.cache_flag:
                data.append(one.file_path)
            await one.delete()
        return data

    @classmethod
    async def reset(cls) -> None:
        """
        重置数据库，将所有记录删除
        """
        await cls.all().delete()
