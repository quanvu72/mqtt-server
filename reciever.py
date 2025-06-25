import time
import os 
import paho.mqtt.client as paho
from paho import mqtt
from datetime import datetime

broker = "192.168.30.28"   
port = 1883
topic_sub = "image/topic"
username = "phuongtrinh" 
password = "Phuong123"

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

def on_message(client, userdata, msg):
    print(" Ảnh nhận được, đang lưu vào file...")
    filename = datetime.now().strftime("received_%H%M%S.jpg")
    with open(filename, "wb") as f:
        f.write(msg.payload)
    print(f" Đã lưu thành file {filename} ({len(msg.payload)} bytes)")
    #print(msg.topic + " " + str(msg.payload))
'''
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
'''

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv311)
client.on_connect = on_connect
#client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
#client.username_pw_set(username, password)
client.connect(broker, port)

client.on_message = on_message

client.subscribe(topic_sub, qos=1)

# Bắt đầu vòng lặp nhận dữ liệu
client.loop_forever()