import asyncio
import json

from comtypes.client import CreateObject, GetEvents, PumpEvents
from psutil import NoSuchProcess, Process


class MessageReporter:
    """
    消息接收器
    """

    def OnGetMessageEvent(self, msg):
        msg = json.loads(msg[0])
        print(msg)


class ComProgress:
    """
    com通讯组件
    """

    robot = None
    """com通讯robot"""
    event = None
    """com通讯event"""
    com_pid: int
    """com进程的pid"""
    wechat_pid: int
    """微信pid"""
    connection_point = None
    """消息接收点"""
    msg_reporter: MessageReporter
    """消息接收器"""

    def __init__(self) -> None:
        self.robot = None
        self.event = None
        self.com_pid = None
        self.wechat_pid = None
        self.connection_point = None
        self.msg_reporter = MessageReporter()

    def init(self) -> None:
        """
        初始化com组件
        """
        try:
            self.robot = CreateObject("WeChatRobot.CWeChatRobot")
            self.event = CreateObject("WeChatRobot.RobotEvent")
            self.com_pid = self.robot.CStopRobotService(0)
        except OSError:
            print("未注册COM通讯组件")
        print("done")

    def close(self) -> None:
        """
        关闭com进程
        """
        if self.com_pid is not None:
            try:
                com_process = Process(self.com_pid)
                com_process.kill()
            except NoSuchProcess:
                pass
        self.com_pid = None

    def register_msg_event(self) -> None:
        """
        注册消息事件
        """
        self.connection_point = GetEvents(self.event, self.msg_reporter)
        self.event.CRegisterWxPidWithCookie(
            self.wechat_pid, self.connection_point.cookie
        )

    def _pump_event(self) -> None:
        """接收event"""
        while True:
            try:
                PumpEvents(2)
            except KeyboardInterrupt as e:
                raise e

    def start_msg_recv(self) -> None:
        """
        开始接收消息
        """
        loop = asyncio.get_event_loop()
        loop.run_in_executor(func=self._pump_event)

    def start_inject(self) -> None:
        """
        开始注入
        """
        pass


if __name__ == "__main__":
    com = ComProgress()
    com.init()
