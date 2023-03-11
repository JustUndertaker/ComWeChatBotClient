import wechatbot_client

wechatbot_client.init()

wechatbot_client.load("wechatbot_client.startup")


if __name__ == "__main__":
    wechatbot_client.run()
