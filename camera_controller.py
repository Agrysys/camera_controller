import paho.mqtt.client as mqtt
import json
import cv2
import requests

def pub_mqtt(message):
    mqttBroker = "mqtt.eclipseprojects.io"
    client = mqtt.Client("wemos")
    client.connect(mqttBroker)

    client.publish("agrysys/conveyor", message)
    print("Just published " + str(message) + " to Topic agrysys/conveyor")

def capture_and_send_image(filename='capture.jpg', url='http://127.0.0.1:8000/ssm/api/v1/predict/class'):
    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        # Read the current frame from the webcam
        ret, frame = cap.read()

        # If the frame was read correctly, save it to a file and break the loop
        if ret:
            cv2.imwrite(filename, frame)
            break

    # Release the webcam
    cap.release()

    # Send the image file to the specified URL
    with open(filename, 'rb') as f:
        files = {'image': f}
        response = requests.post(url, files=files)
        data = json.loads(response.text)
        kelas_value = data["kelas"]
        pub_mqtt(kelas_value)

    # Print the response from the server
    print(response.text)

# Call the function to capture an image and send it



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
client.loop_end()