import asyncio
import logging
import os
import socket

from amqtt.broker import Broker

def get_ipv4_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Chỉ “kết nối giả” tới 8.8.8.8 để lấy IP của card đang dùng
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError as e:
        return f"Lỗi mạng: {e}"
    
broker = get_ipv4_address()

logger = logging.getLogger(__name__)

config = {
    "listeners": {
        "default": {
            "type": "tcp",
            "bind": f"{broker}:1883",
        }
    },
    "sys_interval": 10,
    #"auth": {
    #"allow-anonymous": True
#}
    
    "auth": {
        "allow-anonymous": True,
        "password-file": os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "passwd",
        ),
        "plugins": ["auth_file", "auth_anonymous"],
    },
    "topic-check": {"enabled": False},
}


async def test_coro() -> None:
    broker = Broker(config)
    await broker.start()
    # await asyncio.sleep(5)
    # await broker.shutdown()


if __name__ == "__main__":
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    # formatter = "%(asctime)s :: %(levelname)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(test_coro())
    asyncio.get_event_loop().run_forever()
    # asyncio.run(test_coro())