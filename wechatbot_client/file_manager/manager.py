import asyncio
from pathlib import Path
from shutil import copyfile
from typing import Optional, Tuple
from uuid import uuid4

from httpx import URL, AsyncClient

from wechatbot_client.consts import DOWNLOAD_TIMEOUT, FILE_CACHE
from wechatbot_client.utils import logger_wrapper, run_sync

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

    def get_file_name(self, file_path: Path) -> Path:
        """
        说明:
            对于保存在Temp的文件，为了防止重名，需要更改文件名

        参数:
            * `file_path`: 文件路径

        返回:
            * `Path`: 更改后的文件路径
        """
        count = 0
        original_file_path = file_path
        while file_path.exists():
            count += 1
            file_name = f"{original_file_path.stem}({count}){original_file_path.suffix}"
            file_path = original_file_path.parent / file_name
        return file_path

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
                file_path = self.file_path / name
                file_path = self.get_file_name(file_path)
                with open(file_path, mode="wb") as f:
                    f.write(data)
            except Exception as e:
                log("ERROR", f"文件下载失败:{e}")
                return None

        await FileCache.create_file_cache(
            file_id=file_id, file_path=str(file_path.absolute()), file_name=name
        )
        return file_id

    async def cache_file_id_from_path(
        self, get_path: Path, name: str, copy: bool = True
    ) -> Optional[str]:
        """
        说明:
            从路径缓存一个文件

        参数:
            * `path`: 文件路径
            * `name`: 文件名
            * `copy`: 是否复制到temp下

        返回:
            * `str | None`: 文件id，文件不存在时为None
        """
        if not get_path.exists():
            log("ERROR", "缓存的文件不存在")
            return None
        file_id = str(uuid4())
        if copy:
            file_path = self.file_path / name
            file_path = self.get_file_name(file_path)
            copyfile(get_path, file_path)
        else:
            file_path = get_path
        await FileCache.create_file_cache(
            file_id=file_id,
            file_path=str(file_path.absolute()),
            file_name=name,
            file_temp=copy,
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
        file_path = self.file_path / name
        file_path = self.get_file_name(file_path)
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

    @run_sync
    def clean_tempfile(self, file_paths: list[str]) -> int:
        """
        清理临时文件
        """
        count = 0
        for file_path in file_paths:
            file = Path(file_path)
            if file.exists():
                file.unlink()
                count += 1
        return count

    async def clean_cache(self, days: int = 3) -> int:
        """
        说明:
            清理缓存

        参数:
            * `days`: 清理多少天前的缓存

        返回:
            * `int`: 清理的文件数量
        """
        file_paths = await FileCache.clean_file(days)
        count = await self.clean_tempfile(file_paths)
        log("SUCCESS", f"清理缓存成功，共清理: {count} 个文件...")
        return count

    async def reset_cache(self) -> None:
        """
        重置缓存
        """
        await FileCache.reset()
        for file in self.file_path.iterdir():
            file.unlink()
        log("SUCCESS", "重置文件缓存...")

    async def wait_image_task(self, image_path: str, future: asyncio.Future) -> None:
        """
        等待图片任务
        """
        jpg = Path(f"{image_path}.jpg")
        png = Path(f"{image_path}.png")
        gif = Path(f"{image_path}.gif")
        while True:
            if future.cancelled():
                return
            if jpg.exists():
                future.set_result(jpg)
                return
            if png.exists():
                future.set_result(png)
                return
            if gif.exists():
                future.set_result(gif)
                return
            await asyncio.sleep(0.5)

    async def wait_for_image(self, image_path: str) -> Optional[Path]:
        """
        说明:
            等待图片下载成功
        """
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        loop.create_task(self.wait_image_task(image_path, future))
        try:
            await asyncio.wait_for(future, DOWNLOAD_TIMEOUT)
        except asyncio.TimeoutError:
            log("ERROR", "图片下载超时...")
            future.cancel()
            return None
        return future.result()

    async def wait_file_task(self, file: Path, future: asyncio.Future) -> None:
        """
        等待文件任务
        """
        while True:
            if future.cancelled():
                return
            if file.exists():
                future.set_result(file)
                return
            await asyncio.sleep(0.5)

    async def wait_for_file(self, file: Path) -> Optional[Path]:
        """
        说明:
            等待文件下载成功
        """
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        loop.create_task(self.wait_file_task(file, future))
        try:
            await asyncio.wait_for(future, DOWNLOAD_TIMEOUT)
        except asyncio.TimeoutError:
            log("ERROR", "文件下载超时...")
            future.cancel()
            return None
        return future.result()
