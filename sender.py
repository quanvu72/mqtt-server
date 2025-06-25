from paho.mqtt import client as mqtt
import socket

#from paho import mqtt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
Tk().withdraw()
file_path = askopenfilename(
    title="Chọn ảnh để gửi",
    filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
)

if not file_path:
    print("Chưa chọn ảnh")
    exit()
with open(file_path, "rb") as f:
    data_img = f.read()

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

client = mqtt.Client()
#client.username_pw_set("testuser", "testpass")
client.connect(broker, 1883)
client.publish("image/topic", data_img)
client.disconnect()