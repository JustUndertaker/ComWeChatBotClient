"""
文件管理类，用来映射文件id与path
为了防止文件名冲突，数据库只做映射相关
使用了sqlite数据库
"""

from .manager import FileManager as FileManager
from .model import FileCache as FileCache
from .model import database_close as database_close
from .model import database_init as database_init
