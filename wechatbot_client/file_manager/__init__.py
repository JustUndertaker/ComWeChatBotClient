"""
文件管理类，用来映射文件id与path
为了防止文件名冲突，数据库只做映射相关
使用了sqlite数据库
"""

from .manager import FileManager
