"""
子进程运行wcf.exe
"""
import subprocess

from wechatbot_client.log import logger


def install(cmd_path: str, debug: bool) -> bool:
    """
    说明:
        安装dll注入微信进程

    参数:
        * `cmd_path`: wcf.exe路径
        * `debug`: 是否开启wcf的debug日志

    返回:
        * `bool`: 是否注入成功
    """
    cmd = [cmd_path, "start"]
    if debug:
        cmd.append("debug")
    child = subprocess.run(cmd)
    return child.returncode == 0


def uninstall(cmd_path: str) -> None:
    """
    说明:
        卸载安装的dll注入

    参数:
        * `cmd_path`: wcf.exe路径
    """
    logger.info("<y>正在卸载微信注入...</y>")
    cmd = [cmd_path, "stop"]
    child = subprocess.run(cmd)
    if child.returncode == 0:
        logger.info("<g>微信注入模块卸载完毕...</g>")
    else:
        logger.error("<r>微信注入模块卸载失败...</r>")
