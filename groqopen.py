import cv2
from groq import Groq
import time
import base64

# function to read images = sigma
from groqt import sigma

# Replace "0" with a file path to work with a saved video, right now 0 means webcam/camera!!
stream = cv2.VideoCapture(0)

if not stream.isOpened():
    print("No stream :(")
    exit()  

# what is cap pro fps?
fps = stream.get(cv2.CAP_PROP_FPS)
width = int(stream.get(3))
height = int(stream.get(4))

last_capture_time = time.time()

# to save video
# output = cv2.VideoWriter("assets/4_stream.mp4",
#             cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
#             fps=fps, frameSize=(width, height))

# stream camera to a frame
while True:
    ret, frame = stream.read()
    if not ret: # if no frames are returned
        print("No more stream :(")
        break
    
    frame = cv2.resize(frame, (width, height))
    # output.write(frame)
    cv2.imshow("Webcam!", frame)

    # Capture and save an image every 5 seconds
    current_time = time.time()
    if current_time - last_capture_time >= 5:  # 5 seconds passed
        image_filename = f"snapshot.jpg"
        cv2.imwrite(image_filename, frame)
        print(f"Image saved as {image_filename}")
        last_capture_time = current_time  # Update the last capture time

        # Analyze the newly captured image
        sigma()

        # quit
    if cv2.waitKey(1) == ord('q'): # press "q" to quit
        break

stream.release()
cv2.destroyAllWindows() #!
