import paho.mqtt.client as mqtt
import requests
import cv2
import numpy as np
import imutils
import json

from scipy.ndimage import zoom

# MQTT setup
mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("laptop")
client.connect(mqttBroker)

# Camera setup
camera_ip = "192.168.100.4"
camera_url = f"http://{camera_ip}:8080/shot.jpg"
scale = 1.0

def on_message(client, userdata, message):
    # Capture and send image when a message is received
    capture_and_send_image()
    print("Received message: ", str(message.payload.decode("utf-8")))

def pub_mqtt(message):
    client = mqtt.Client("wemos")
    client.connect(mqttBroker)

    client.publish("agrysys/servo", message)
    print("Just published " + str(message) + " to Topic agrysys/conveyor")

def clipped_zoom(img, zoom_factor):
    h, w = img.shape[:2]

    # For multichannel images we don't want to apply the zoom factor to the RGB
    # dimension, so instead we create a tuple of zoom factors, one per array
    # dimension, with 1's for any trailing dimensions after the width and height.
    zoom_tuple = (zoom_factor,) * 2 + (1,) * (img.ndim - 2)

    # Zooming out
    if zoom_factor < 1:
        # Bounding box of the zoomed-out image within the output array
        zh = int(np.round(h * zoom_factor))
        zw = int(np.round(w * zoom_factor))
        top = (h - zh) // 2
        left = (w - zw) // 2

        # Zero-padding
        out = np.zeros_like(img)
        out[top:top+zh, left:left+zw] = zoom(img, zoom_tuple)

    # Zooming in
    elif zoom_factor > 1:
        # Bounding box of the zoomed-in region within the input array
        zh = int(np.round(h / zoom_factor))
        zw = int(np.round(w / zoom_factor))
        top = (h - zh) // 2
        left = (w - zw) // 2

        out = zoom(img[top:top+zh, left:left+zw], zoom_tuple)

        # `out` might still be slightly larger than `img` due to rounding, so
        # trim off any extra pixels at the edges
        trim_top = ((out.shape[0] - h) // 2)
        trim_left = ((out.shape[1] - w) // 2)
        out = out[trim_top:trim_top+h, trim_left:trim_left+w]

    # If zoom_factor == 1, just return the input array
    else:
        out = img
    return out

def take_ipcam_picture(url_ip_cam):
    img_resp = requests.get(url_ip_cam) 
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8) 
    img = cv2.imdecode(img_arr, -1) 
    img = imutils.resize(img, width=int(1000*scale), height=int(1800*scale))
    img_path = "img/Android_cam.jpg"
    cv2.imwrite(img_path, img)
    print("Image saved!")
    return img_path


def capture_and_send_image(url='http://127.0.0.1:8000/ssm/api/v1/predict/class'):

    img_path = take_ipcam_picture(camera_url)
    
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


client.loop_start()
client.subscribe("agrysys/camera")
client.on_message = on_message
while True:
    img_resp = requests.get(camera_url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = imutils.resize(img, width=int(1000), height=int(1800))
    # img = clipped_zoom(img,2.5)
    cv2.imshow("Android_cam", img)

    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break
    
    # Zoom in with '+' key
    if cv2.waitKey(1) == ord('i'):
        scale += 0.1

    # Zoom out with '-' key
    if cv2.waitKey(1) == ord('o'):
        scale -= 0.1

cv2.destroyAllWindows()
client.loop_stop()
