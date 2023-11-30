import cv2
import numpy as np

def zoom_in_video(input_video_path, output_video_path, zoom_scale=2.0):
    # Open the video file
    video = cv2.VideoCapture(input_video_path)

    # Get the original video's width, height, and frames per second (fps)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    while(video.isOpened()):
        ret, frame = video.read()
        if ret:
            # Get the size of the image
            h, w, _ = frame.shape

            # Define the zoomed frame
            zoomed_frame = cv2.resize(frame, None, fx=zoom_scale, fy=zoom_scale)

            # Get the size of the zoomed image
            zh, zw, _ = zoomed_frame.shape

            # Define the region of interest in the zoomed image
            roi = zoomed_frame[int((zh-h)/2):int((zh+h)/2), int((zw-w)/2):int((zw+w)/2)]

            # Write the ROI to the output file
            out.write(roi)
        else:
            break

    # Release everything when done
    video.release()
    out.release()
    cv2.destroyAllWindows()

# Use the function
zoom_in_video('video\Video WhatsApp 2023-11-29 pukul 22.11.52_59fe4796.mp4', 'video/output.mp4')
