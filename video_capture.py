import cv2


camera_ip = "192.168.100.4"
camera_url = f"http://{camera_ip}:8080/video"
# Create a VideoCapture object
cap = cv2.VideoCapture(camera_url)

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
