"""
微信客户端抽象，整合各种请求需求:
 - 处理`driver`: 上下发送请求
 - 处理`com_wechat`: 维护与comwechat的连接
 - 处理`api`: 处理api调用
"""
from .wechat import WeChatManager as WeChatManager
