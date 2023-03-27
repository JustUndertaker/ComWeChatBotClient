"""
文件路由器，此文件实现了`get_file`的通过`url`获取文件的功能
"""
from fastapi import APIRouter
from fastapi.responses import FileResponse, Response

from wechatbot_client.file_manager import FileCache

router = APIRouter()


@router.get("/get_file/{file_id}")
async def get_file_get(file_id: str) -> FileResponse:
    """
    通过url获取文件
    """
    file_path, file_name = await FileCache.get_file(file_id)
    if file_path is None:
        return Response(status_code=404, content="File not found")
    return FileResponse(path=file_path, filename=file_name)


@router.post("/get_file/{file_id}")
async def get_file_post(file_id: str) -> FileResponse:
    """
    通过url获取文件
    """
    file_path, file_name = await FileCache.get_file(file_id)
    if file_path is None:
        return Response(status_code=404, content="File not found")
    return FileResponse(path=file_path, filename=file_name)
