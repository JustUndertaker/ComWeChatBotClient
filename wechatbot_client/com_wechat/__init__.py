"""
与微信通信底层
注入步骤：
创建com对象 -> 检测微信进程 -> 注入
创建com对象 -> 未检测到微信进程 -> 创建微信进程 -> 注入

调用消息:
http/ws -> wechat -> comprocess -> com

上报消息:
com -> msgreporter -> wechat -> http/ws
"""

from .com_wechat import ComWechatApi as ComWechatApi
from .message import MessageHandler as MessageHandler
from .model import Message as Message
