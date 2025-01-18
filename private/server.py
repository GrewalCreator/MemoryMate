import datetime
import os
from flask import Flask, request, jsonify
import cv2
import numpy as np
from threading import Lock
from collections import deque
from groqAI import facial_recognition
import requests
import time
import threading

app = Flask(__name__)

# Circular queue for frames
QUEUE_SIZE = 10
frame_queue = deque(maxlen=QUEUE_SIZE)  # Circular buffer to hold frames
frame_lock = Lock()
FRAME_SEQ = 0

# Frame rate limiting (e.g., 15 FPS)
FRAME_RATE_LIMIT = 1 / 15
last_processed_time = 0
SAVE_DIR = './received_frames'  # Directory to save frames
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route('/api/live-feed', methods=['POST'])
def live_feed():
    global FRAME_SEQ
    """Endpoint to receive frames from the camera and enqueue them."""
    if 'video' not in request.files:
        return "No video stream found in request", 400

    video_file = request.files['video']
    video_stream = video_file.read()
    nparr = np.frombuffer(video_stream, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if frame is not None:
        # Optional: Add to queue for further processing
        with frame_lock:
            frame_queue.append(frame)
            frame, FRAME_SEQ = facial_recognition(frame, FRAME_SEQ)
        
        frame_filename = os.path.join(SAVE_DIR, f'frame.jpg')
        cv2.imwrite(frame_filename, frame)

    return "Frame received", 200

@app.route('/api/get-frames', methods=['GET'])
def get_frames():
    """Endpoint to fetch all frames currently in the queue."""
    with frame_lock:
        frames = list(frame_queue)
        encoded_frames = []

        for frame in frames:
            _, buffer = cv2.imencode('.jpg', frame)
            encoded_frames.append(buffer.tobytes())

    # Return all frames as a list of base64-encoded JPEGs
    return jsonify({"frames": [frame.hex() for frame in encoded_frames]})

'''
def test_send_camera_frames():
    """Test function to send frames from the laptop camera."""
    camera = cv2.VideoCapture(0)  # Open the default camera
    if not camera.isOpened():
        print("Unable to access the camera")
        return

    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                print("Failed to read frame from camera")
                break

            _, buffer = cv2.imencode('.jpg', frame)
            response = requests.post(
                'http://127.0.0.1:5000/api/live-feed',  # Update with your server's URL
                files={'video': ('frame.jpg', buffer.tobytes(), 'image/jpeg')}
            )

            print(f"Frame sent: {response.status_code}")
            time.sleep(0.1)  # Limit sending to ~10 FPS
    except KeyboardInterrupt:
        print("Test interrupted")
    finally:
        camera.release()
        print("Camera released")
'''
        
if __name__ == "__main__":
    # Start the test function for laptop camera in a separate thread
    # threading.Thread(target=test_send_camera_frames, daemon=True).start()

    # Run the Flask server
    app.run(host='0.0.0.0', port=5000)
