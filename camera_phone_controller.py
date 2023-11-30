import paho.mqtt.client as mqtt
import json
import cv2
import requests
import urllib.request
import ssl
import numpy as np
import imutils

def take_ipcam_picture(url_ip_cam):
    img_resp = requests.get(url_ip_cam) 
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8) 
    img = cv2.imdecode(img_arr, -1) 
    img = imutils.resize(img, width=1000, height=1800) 
    img_path = "Android_cam.jpg"
    cv2.imwrite(img_path, img)
    print("Image saved!")
    return img_path



def pub_mqtt(message):
    mqttBroker = "mqtt.eclipseprojects.io"
    client = mqtt.Client("wemos")
    client.connect(mqttBroker)

    client.publish("agrysys/servo", message)
    print("Just published " + str(message) + " to Topic agrysys/conveyor")

def capture_and_send_image(filename='capture.jpg', url='http://127.0.0.1:8000/ssm/api/v1/predict/class'):
    video_url = 'http://10.10.181.67:8080/shot.jpg'

    img_path = take_ipcam_picture(video_url)
    
    with open(img_path, 'rb') as f:
        files = {'image': f}
        response = requests.post(url, files=files)
        data = json.loads(response.text)
        kelas_value = data["kelas"]
        if kelas_value == "BM":
            pub_mes = 0
        elif kelas_value == "MM":
            pub_mes = 2
        else:
            pub_mes = 1
        pub_mqtt(pub_mes)

    # Print the response from the server
    print(response.text)

def on_message(client, userdata, message):
    capture_and_send_image()
    print("Received message: ", str(message.payload.decode("utf-8")))

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("laptop")
client.connect(mqttBroker)

client.loop_start()
client.subscribe("agrysys/camera")
client.on_message = on_message
input("Press Enter to stop the loop...")
client.loop_stop()