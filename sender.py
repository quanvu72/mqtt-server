from paho.mqtt import client as mqtt

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
    print("Đã gửi...")
    data_img = f.read()


client = mqtt.Client()
#client.username_pw_set("testuser", "testpass")
client.connect("192.168.30.28", 1883)
client.publish("image/topic", data_img)
client.disconnect()