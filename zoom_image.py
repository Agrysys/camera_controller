import cv2
import numpy as np

def zoom_image(img_path, zoom_factor):
    # Load the image
    img = cv2.imread(img_path)

    # Get the original image size
    height, width = img.shape[:2]

    # The new image size should be zoom_factor times the original size
    new_height, new_width = int(height * zoom_factor), int(width * zoom_factor)

    # Resize the image
    zoomed_img = cv2.resize(img, (new_width, new_height), interpolation = cv2.INTER_LINEAR)

    return zoomed_img

zoomed_img = zoom_image('img\Android_cam.jpg', 2)
cv2.imshow('Zoomed Image', zoomed_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
