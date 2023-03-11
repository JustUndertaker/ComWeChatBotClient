"""
启动行为管理，将各类业务剥离开
"""
from wechatbot_client import get_driver
from wechatbot_client.com.http import router
from wechatbot_client.log import logger

driver = get_driver()


@driver.on_startup
async def start_up() -> None:
    """
    启动行为管理
    """
    driver.server_app.include_router(router)
    logger.success("<g>http api已开启...</g>")
