import cv2
from flask_cors import CORS
import numpy as np
from threading import Lock
from collections import deque

import requests
from groqAI import facial_recognition
import time
from flask import Flask, Response, request, jsonify, send_from_directory
import os

from database.mongo import MongoDBClient

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'  # Directory to store images
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Circular queue for frames and pending approvals
QUEUE_SIZE = 10
frame_queue = deque(maxlen=QUEUE_SIZE)
pending_approval = deque(maxlen=QUEUE_SIZE)

# Locks to manage concurrent access
frame_lock = Lock()
image_lock = Lock()

FRAME_SEQ = 0
SAVED_IMG = 0

FRAME_RATE_LIMIT = 1 / 15
last_processed_time = 0

@app.route('/api/live-feed', methods=['POST'])
def live_feed():
    global FRAME_SEQ, SAVED_IMG
    if 'video' not in request.files:
        return jsonify({"error": "No video stream found in request"}), 400

    video_file = request.files['video']
    video_stream = video_file.read()
    nparr = np.frombuffer(video_stream, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    new_user_url = ""

    if frame is not None:
        if not hasattr(live_feed, "rectangle"):
            live_feed.rectangle = None
        if not hasattr(live_feed, "frames"):
            live_feed.frames = 0
        if not hasattr(live_feed, "count"):
            live_feed.count = 0

        with frame_lock:
            frame, live_feed.rectangle, live_feed.frames, live_feed.count, new_user_url = facial_recognition(
                frame, live_feed.rectangle, live_feed.frames, live_feed.count
            ) or (frame, None, 0, 0, None)

            print(f'UNKNOWN: {new_user_url}')

            

            # Save frame as image and store its path in approval queue
            #image_filename = f"{UPLOAD_FOLDER}/frame_{int(time.time())}.jpg"

            image_filename = f"{UPLOAD_FOLDER}/frame.jpg"
            cv2.imwrite(image_filename, frame)
            frame_queue.append(image_filename)

            with image_lock:
                if len(pending_approval) < QUEUE_SIZE and new_user_url:
                    pending_approval.append(new_user_url)
                    print(f'URL QUEQUE: {pending_approval}')

    return jsonify({"message": "Frame received"}), 200



@app.route('/api/stream', methods=['GET'])
def get_stream():
    with frame_lock:
        if not frame_queue:
            return jsonify({"message": "No images available"}), 204  # No content available

        image_path = frame_queue.popleft()
        public_url = f"http://localhost:5000/uploads/{os.path.basename(image_path)}"

    return jsonify({"image_path": public_url}), 200

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/api/get-image', methods=['GET'])
def get_image():
    print("LOOKING FOR NEW PERSON")
    """Send the next image URL to the frontend for approval."""
    with image_lock:
        if not pending_approval:
            return jsonify({"message": "No images available"}), 204  # No content available

        image_path = pending_approval.popleft()
        image_url = f"http://{request.host}/{image_path}"  # Generate public URL

    return jsonify({"image_url": image_url}), 200

@app.route('/uploads/<filename>', methods=['GET'])
def serve_image(filename):
    """Serve image files from the uploads folder."""
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/api/approve', methods=['POST'])
def approve_image():
    """Handle image approval from frontend."""
    data = request.get_json()
    if not data or 'name' not in data or 'description' not in data or 'relation' not in data:
        return jsonify({"error": "Missing fields"}), 400

    # Process the approval (simulate saving the approved image details)
    mongoDBClient = MongoDBClient()
    mongoDBClient.approve(data['name'], data['description'], data['relation'])

    return jsonify({"message": "Image approved successfully"}), 200

@app.route('/api/deny', methods=['POST'])
def deny_image():
    """Handle image denial from frontend."""
    data = request.get_json()
    if not data or 'action' not in data:
        return jsonify({"error": "Invalid request"}), 400
    
    mongoDBClient = MongoDBClient()
    mongoDBClient.deny()

    return jsonify({"message": "Image denied successfully"}), 200


@app.route('/api/get-images', methods=['GET'])
def get_images():
    mongoClient = MongoDBClient()
    allPhotos = mongoClient.getAllPhotos()
    for photo in allPhotos:
        imageUrl = photo["images"][0]
    return jsonify(allPhotos)

@app.route('/api/get-new-images', methods=['GET'])
def get_imagees():
    mongoClient = MongoDBClient()
    allPhotos = mongoClient.getAllPhotos()
    new = None
    for photo in allPhotos:
        if photo["name"] is None:
            new = photo["images"][0]
            break
    return jsonify(new)

if __name__ == "__main__":
    # before we run the app, we cache the images
    mongoClient = MongoDBClient()
    allPhotos = mongoClient.getAllPhotos()
    print(allPhotos)
    # Ensure the directory exists
    output_dir = 'images'
    os.makedirs(output_dir, exist_ok=True)

    index = 0  # Assuming index starts from 0
    for photo in allPhotos:
        img_url = requests.get(photo["images"][0]).content
        img_name = os.path.join(output_dir, f"{index}.jpg")
        with open(img_name, 'wb') as img_file:
            img_file.write(img_url)
        index += 1

    app.run(host='0.0.0.0', port=5000)