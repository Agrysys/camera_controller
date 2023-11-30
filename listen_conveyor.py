import paho.mqtt.client as mqtt
import time
import cv2
import requests


def on_message(client, userdata, message):
    print("Received message: ", str(message.payload.decode("utf-8")))

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("webcame")
client.connect(mqttBroker)

client.loop_start()
client.subscribe("agrysys/camera")
client.on_message = on_message
input("Press Enter to stop the loop...")
client.loop_stop()
