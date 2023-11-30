import cv2
from gpuvid.UMatFileVideoStream import UMatFileVideoStream

video = UMatFileVideoStream("video\input.mp4", 1).start()
rgb = cv2.UMat(self.height, self.width, cv2.CV_8UC3)
while not video.stopped:
    cv2.cvtColor(video.read(), cv2.COLOR_BGR2RGB, hsv, 0)
    # more of processing before fetching the images
    cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB, hsv, 0)
    img = hsv.get()   # image is now a numpy array