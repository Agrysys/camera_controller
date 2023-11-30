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
video_url = f"http://{camera_ip}:8080/video"
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
    zoom_tuple = (zoom_factor,) * 2 + (1,) * (img.ndim - 2)

    if zoom_factor < 1:
        zh = int(np.round(h * zoom_factor))
        zw = int(np.round(w * zoom_factor))
        top = (h - zh) // 2
        left = (w - zw) // 2

    elif zoom_factor > 1:
        zh = int(np.round(h / zoom_factor))
        zw = int(np.round(w / zoom_factor))
        top = (h - zh) // 2
        left = (w - zw) // 2

        # out = zoom(img[top:top+zh, left:left+zw], zoom_tuple)
        trim_top = top
        trim_left = left

    else:
        trim_top = 0
        trim_left = 0

    return trim_top,trim_top+zh, trim_left, trim_left+zw, zoom_tuple


def take_ipcam_picture(url_ip_cam):
    img_resp = requests.get(url_ip_cam) 
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8) 
    img = cv2.imdecode(img_arr, -1) 
    img = imutils.resize(img, width=int(1000*scale), height=int(1800*scale))
    zoom_frame = zoom(img[y1:x1, y2:x2], zoom_tuple)
    img_path = "img/Android_cam.jpg"
    cv2.imwrite(img_path, zoom_frame)
    print("Image saved!")
    return img_path


def capture_and_send_image(url='http://127.0.0.1:8000/ssm/api/v1/predict/class'):

    img_path = take_ipcam_picture(camera_url)
    
    with open(img_path, 'rb') as f:
        files = {'image': f}
        # response = requests.post(url, files=files)
        # data = json.loads(response.text)
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

img = cv2.imread("img\Android_cam.jpg")
y1,x1,y2,x2,zoom_tuple = clipped_zoom(img,2)

client.loop_start()
client.subscribe("agrysys/camera")
client.on_message = on_message
# Create a VideoCapture object
cap = cv2.VideoCapture(video_url)

# Check if camera opened successfully
if not cap.isOpened(): 
    print("Unable to read camera feed")

# Default resolutions of the frame are obtained.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the codec and create a VideoWriter object.
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

while(True):
  ret, frame = cap.read()


  if cv2.waitKey(1) == 27:
        break
  if ret: 
    # Write the frame into the file 'output.avi'
    out.write(frame)
    # zoom_frame = zoom(frame[y1:x1, y2:x2], zoom_tuple)
    # Display the resulting frame    
    cv2.imshow('frame',frame)

    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  else:
    break

# When everything done, release the video capture and video write objects
cap.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows() 