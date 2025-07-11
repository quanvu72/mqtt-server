import logging
import asyncio
import socket
import os
import json
import paho.mqtt.client as paho
from paho import mqtt
from datetime import datetime
from amqtt.broker import Broker
from amqtt.client import MQTTClient
from amqtt.mqtt.constants import QOS_1

# Cấu hình logger để hiển thị thông tin
formatter = "[%(asctime)s] :: %(levelname)s :: %(message)s"
logging.basicConfig(level=logging.INFO, format=formatter)
logger = logging.getLogger(__name__)
latest_messages = {}

img_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")

log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "log")
log_file = datetime.now().strftime("%d%m_%H%M%S_log.json")
log_path = os.path.join(log_dir, log_file)

def load_log():
    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"clients": {}, "messages": []}
    else:
        return {"clients": {}, "messages": []}

def save_log(log_data):
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False, default=str)

def log_client_connection(client_id, client_address, conn_time):
    log_data = load_log()
    log_data["clients"][client_id] = {
        "client_address": client_address,
        "conn_time": conn_time
    }
    save_log(log_data)

def log_message(topic, payload, timestamp):
    log_data = load_log()
    log_data["messages"].append({
        #"client_id": client_id,
        "topic": topic,
        "payload": payload,
        "timestamp": timestamp
    })
    save_log(log_data)

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
config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': f'{broker}:1883',
        },
    },
    'sys_interval': 10,
    'auth': {
        'allow-anonymous': True,
        'password-file': "passwd",
        'plugins': ['auth_anonymous']
    }
}

async def client_manager(broker):
    known_clients = set()
    while True:
        await asyncio.sleep(3)
        sessions = broker.sessions
        if sessions:
            logger.info("==================================================================")
            logger.info(f"Client connected: {len(sessions)}")
            for client_id, session_tuple in sessions.items():
                session = session_tuple[0]
                logger.info(f" - Client ID: {client_id}")
                address = getattr(session, 'client_address', None)
                conn_time = getattr(session, 'conn_time', None)
                logger.info(f"   connect from: {address}")
                logger.info(f"   connect time: {conn_time}")
                # Ghi log client mới nếu chưa có
                if client_id not in known_clients:
                    log_client_connection(client_id, address, conn_time)
                    known_clients.add(client_id)
                msg = latest_messages.get(client_id)
                if msg:
                    logger.info(f"   Latest message: {msg}")
            logger.info("==================================================================")
        else:
            logger.info("No clients connected.")

async def brokerGetMessage():
    C = MQTTClient(client_id="get_message_client")
    await C.connect(f'mqtt://{broker}:1883')
    await C.subscribe([
        ("#", QOS_1)
    ])
    #logger.info('Subscribed all!')
    try:
        while True:
            message = await C.deliver_message()
            packet = message.publish_packet
            payload = packet.payload.data#.decode('utf-8')
            topic = packet.variable_header.topic_name
            is_image = False

            # Nhận diện topic chứa ảnh (ví dụ: images/ hoặc topic_sub của bạn)
            if topic.startswith("images/") or topic.startswith("image/") or topic.endswith("/image"):
                is_image = True
            if is_image:
                filename = datetime.now().strftime("%d%m_%H%M%S_img.jpg")
                file_path = os.path.join(img_dir, filename)
                with open(file_path, "wb") as f:
                    f.write(payload)
                logger.info(f"Image received on topic [{topic}], save as {filename} ({len(payload)} bytes)")
                log_message(topic, "image saved as {}".format(filename), datetime.now().isoformat())
            else:
                try:
                    msg_text = payload.decode("utf-8")
                except Exception:
                    msg_text = str(payload)
                logger.info(f"Message and topic [{topic}]: {msg_text}")
                log_message(topic, msg_text, datetime.now().isoformat())
            #logger.info(f"Message and topic [{topic}]: {payload}")
            #log_message(topic, payload, datetime.now().isoformat())
    except Exception as ce:
        logger.error("Client exception : %s" % ce)

async def main():
    broker = Broker(config)
    await broker.start()
    logger.info("Server start...")
    
    task1 = asyncio.create_task(client_manager(broker))
    task2 = asyncio.create_task(brokerGetMessage())

    await asyncio.gather(task1, task2)
    
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
        asyncio.run(main())
        '''asyncio.get_event_loop().run_until_complete(main())
        asyncio.get_event_loop().run_until_complete(brokerGetMessage())
        asyncio.get_event_loop().run_forever()'''