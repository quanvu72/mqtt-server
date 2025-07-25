import logging
import os
import sqlite3
import asyncio
from datetime import datetime
from sqlite3.dbapi2 import connect
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from PIL import Image

logger = logging.getLogger(__name__)

sql_create_table = """
    CREATE TABLE IF NOT EXISTS img (
        client_id text,
        topic text,
        payload text,
        connected_time timestamp
    )
"""
sql_insert = f"""
        INSERT INTO img (client_id, topic, payload, connected_time)
        VALUES (?, ?, ?, ?)
"""


async def insert_image(client_id, topic, payload, connected_time):
    try:
        conn = connect('mqttgit.db')
        c = conn.cursor()
        c.execute(sql_create_table)
        c.execute(sql_insert, (client_id, topic, payload, connected_time))
        conn.commit()
        logger.info(f"Data inserted successfully: {client_id}, {topic}, {payload}, {connected_time}")
    except Exception as e:
        logger.error(f"Insert error: {e}")
    finally:
        conn.close()    


'''c.execute(sql_create_table)
conn.commit()
'''
'''for i in range(1, 100):
    sensor_id = f"sensor_{i}"
    topic = f"iot/sensor_{i}/temp"
    value = round(random.uniform(20.0, 35.0), 2)
    connect_time = datetime.now()
    time.sleep(1)
    sql_insert = f"""
        INSERT INTO mqtt (client_id, topic, payload, connected_time)
        VALUES ('{sensor_id}', '{topic}', '{value}', '{connect_time}')
    """
    c.execute(sql_insert)
    '''

'''try:
    #c.execute(sql_create_table)
    #c.execute(sql_insert)
    conn.commit()
except:
    print("Error occurred")
'''

'''
# select img from database
c.execute("SELECT payload FROM img WHERE client_id = 'image_20250715_173140.jpg'")
result = c.fetchone()

if result:
    img_path = result[0]
    if os.path.exists(img_path):
        with open(img_path, 'rb') as f:
            img_data = f.read()
            print(f"Image data read successfully from {img_path} ({len(img_data)} bytes)")
    else:
        print(f"Image file {img_path} does not exist.")
else:
    print("No image found in the database with the specified client_id.")

img = Image.open(img_path)
img.show()
'''