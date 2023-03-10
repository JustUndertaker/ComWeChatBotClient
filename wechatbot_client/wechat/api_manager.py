import time
from pathlib import Path

from wechatbot_client.com_wechat import ComWechatApi
from wechatbot_client.log import logger
from wechatbot_client.model import Request, Response
from wechatbot_client.utils import escape_tag


class ApiManager:
    """
    api管理器，负责与grpc沟通调用api
    """

    api: ComWechatApi

    def __init__(self) -> None:
        self.api = ComWechatApi()

    def init(self) -> None:
        """
        初始化com
        """
        # 初始化com组件
        logger.debug("<y>初始化com组件...</y>")
        if not self.api.init():
            logger.error("<r>未注册com组件，启动失败...</r>")
            exit(0)
        logger.debug("<g>com组件初始化成功...</g>")
        # 启动微信进程
        logger.debug("<y>正在初始化微信进程...</y>")
        if not self.api.init_wechat_pid():
            logger.error("<r>微信进程启动失败...</r>")
            self.api.close()
            exit(0)
        logger.debug("<g>找到微信进程...</g>")
        # 注入dll
        logger.debug("<y>正在注入微信...</y>")
        if not self.api.start_service():
            logger.error("<r>微信进程启动失败...</r>")
            self.api.close()
            exit(0)
        logger.success("<g>dll注入成功...</g>")
        # 等待登录
        logger.info("<y>等待登录...</y>")
        if not self.wait_for_login():
            logger.info("<g>进程关闭...</g>")
            self.api.close()
            exit(0)
        logger.success("<g>登录完成...</g>")

    def wait_for_login(self) -> bool:
        """
        等待登录
        """
        while True:
            try:
                if self.api.is_wechat_login():
                    return True
                time.sleep(1)
            except KeyboardInterrupt:
                return False

    def _register_msg_event(self) -> None:
        """
        注册消息事件
        """
        ...

    def open_recv_msg(self, file_path: str) -> None:
        """
        注册接收消息
        """
        # 注册消息事件
        self.api.register_msg_event()
        logger.debug("<g>注册消息事件成功...</g>")
        # 启动消息hook
        result = self.api.start_receive_message()
        if not result:
            logger.error("<r>启动消息hook失败...</r>")
        logger.debug("<g>启动消息hook成功...</g>")
        # 启动图片hook
        file = Path(file_path)
        img_file = file / "image"
        result = self.api.hook_image_msg(str(img_file.absolute()))
        if not result:
            logger.error("<r>启动图片hook失败...</r>")
        logger.debug("<g>启动图片hook成功...</g>")
        # 启动语音hook
        voice_file = file / "voice"
        result = self.api.hook_voice_msg(str(voice_file.absolute()))
        if not result:
            logger.error("<r>启动语音hook失败...</r>")
        logger.debug("<g>启动语音hook成功...</g>")
        # 开始监听
        self.api.start_msg_recv()
        logger.info("<g>开始监听消息...</g>")

    def close(self) -> None:
        """
        关闭
        """
        self.api.close()

    def get_wxid(self) -> str:
        """
        获取wxid
        """
        info = self.api.get_self_info()
        return info["wxId"]

    def request(self, request: Request) -> Response:
        """
        说明:
            发送请求，获取返回值

        参数:
            * `request`: 请求体

        返回:
            * `response`: 返回值
        """
        func = getattr(self.api, request.action)
        try:
            result = func(**request.params)
        except Exception as e:
            logger.error(f"<r>调用api错误: {e}</r>")
            return Response(status=500, msg="内部服务错误...", data={})
        logger.debug(f"<g>调用api成功，返回:</g> {escape_tag(str(result))}")
        return Response(status=200, msg="请求成功", data=result)
