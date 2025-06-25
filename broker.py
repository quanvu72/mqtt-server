import asyncio
import logging
import os

from amqtt.broker import Broker

logger = logging.getLogger(__name__)

config = {
    "listeners": {
        "default": {
            "type": "tcp",
            "bind": "192.168.30.28:1883",
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
