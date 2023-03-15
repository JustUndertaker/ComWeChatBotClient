from pathlib import Path
from shutil import copyfile
from typing import Optional, Tuple
from uuid import uuid4

from httpx import URL, AsyncClient

from wechatbot_client.consts import FILE_CACHE
from wechatbot_client.utils import logger_wrapper

from .model import FileCache

log = logger_wrapper("File Manager")


class FileManager:
    """
    文件管理模块
    """

    file_path: Path
    """文件缓存地址"""

    def __init__(self) -> None:
        self.file_path = Path(f"./{FILE_CACHE}/temp")
        self.file_path.mkdir(parents=True, exist_ok=True)

    async def cache_file_id_from_url(
        self, url: str, name: str, headers: dict = None
    ) -> Optional[str]:
        """
        说明:
            下载文件并缓存

        参数:
            * `url`: 文件url地址
            * `name`: 文件名
            * `headers`: 下载添加的header

        返回:
            * `str | None`: 文件id，下载失败为None
        """
        file_url = URL(url)
        if headers is None:
            headers = {}
        async with AsyncClient(headers=headers) as client:
            try:
                res = await client.get(file_url)
                data = res.content
                file_id = str(uuid4())
                file_path = self.file_path / f"{file_id}{name}"
                with open(file_path, mode="wb") as f:
                    f.write(data)
            except Exception as e:
                log("ERROR", f"文件下载失败:{e}")
                return None

        await FileCache.create_file_cache(
            file_id=file_id, file_path=str(file_path.absolute()), file_name=name
        )
        return file_id

    async def cache_file_id_from_path(self, get_path: Path, name: str) -> Optional[str]:
        """
        说明:
            从路径缓存一个文件

        参数:
            * `path`: 文件路径
            * `name`: 文件名

        返回:
            * `str | None`: 文件id，文件不存在时为None
        """
        if not get_path.exists():
            log("ERROR", "缓存的文件不存在")
            return None
        file_id = str(uuid4())
        file_path = self.file_path / f"{file_id}{name}"
        copyfile(get_path, file_path)
        await FileCache.create_file_cache(
            file_id=file_id,
            file_path=str(file_path.absolute()),
            file_name=name,
        )
        return file_id

    async def cache_file_id_from_data(self, data: bytes, name: str) -> str:
        """
        说明:
            从data缓存文件

        参数:
            * `data`: 文件数据
            * `name`: 文件名

        返回:
            * `str | None`
        """
        file_id = str(uuid4())
        file_path = self.file_path / f"{file_id}{name}"
        with open(file_path, mode="wb") as f:
            f.write(data)
        await FileCache.create_file_cache(
            file_id=file_id, file_path=str(file_path.absolute()), file_name=name
        )
        return file_id

    async def get_file(self, file_id: str) -> Optional[Tuple[str, str]]:
        """
        通过file_id获取文件
        """
        return await FileCache.get_file(file_id)

    async def clean_cache(self, days: int = 3) -> None:
        """
        清理缓存
        """
        file_list = await FileCache.clean_file(days)
        length = len(file_list)
        for file in file_list:
            Path(file).unlink(True)
        log("SUCCESS", f"清理缓存成功，共清理: {length} 个文件...")

    async def reset_cache(self) -> None:
        """
        重置缓存
        """
        await FileCache.reset()
        for file in self.file_path.iterdir():
            file.unlink()
        log("SUCCESS", "重置文件缓存...")
