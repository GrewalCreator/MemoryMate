import datetime
import os
from flask import Flask, Response, request, jsonify
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
frame_queue = deque(maxlen=QUEUE_SIZE)
frame_lock = Lock()
FRAME_SEQ = 0
SAVED_IMG = 0

FRAME_RATE_LIMIT = 1 / 15
last_processed_time = 0




@app.route('/api/live-feed', methods=['POST'])
def live_feed():
    global FRAME_SEQ
    global SAVED_IMG
    if 'video' not in request.files:
        return "No video stream found in request", 400

    video_file = request.files['video']
    video_stream = video_file.read()
    nparr = np.frombuffer(video_stream, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if frame is not None:
        if not hasattr(live_feed, "rectangle"):
            live_feed.rectangle = None
        if not hasattr(live_feed, "frames"):
            live_feed.frames = 0
        if not hasattr(live_feed, "count"):
            live_feed.count = 0

        with frame_lock:
            frame, live_feed.rectangle, live_feed.frames, live_feed.count = facial_recognition(
                frame, live_feed.rectangle, live_feed.frames, live_feed.count
            )
            frame_queue.append(frame)

    return "Frame received", 200


def generate_stream():
    """Stream frames as a multipart/x-mixed-replace response."""
    while True:
        with frame_lock:
            if frame_queue:
                frame = frame_queue[-1]  # Get the latest frame
                _, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            else:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + b'\r\n')



@app.route('/api/get-frames', methods=['GET'])
def get_frames():
    """Stream video frames to the client."""
    return Response(generate_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
