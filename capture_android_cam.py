# Import essential libraries 
import requests 
import cv2 
import numpy as np 
import imutils 

# Replace the below URL with your own. Make sure to add "/shot.jpg" at last. 
url = "http://192.168.100.4:8080/shot.jpg"

# Fetching data from the Url 
img_resp = requests.get(url) 
img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8) 
img = cv2.imdecode(img_arr, -1) 
img = imutils.resize(img, width=1000, height=1800) 

# Save the image
cv2.imwrite('Android_cam.jpg', img)

print("Image saved!")
