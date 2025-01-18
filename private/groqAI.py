import os
import cv2
from dotenv import load_dotenv
import numpy as np
import base64
from groq import Groq

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "cached_frames")
load_dotenv(dotenv_path="./.env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in the environment variables. Ensure .env is correctly configured.")

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))

    center_face = None
    distance_center_face = float('inf')

    for (x, y, w, h) in faces:
        face_mid_x = x + w / 2
        face_mid_y = y + h / 2
        center_x = vid.shape[1] / 2
        center_y = vid.shape[0] / 2
        distance = ((face_mid_x - center_x) ** 2 + (face_mid_y - center_y) ** 2) ** 0.5
        if distance < distance_center_face:
            distance_center_face = distance
            center_face = (x, y, x + w, y + h)

    if center_face:
        x1, y1, x2, y2 = center_face
        cv2.rectangle(vid, (x1, y1), (x2, y2), (0, 255, 0), 4)
        expanded_x1 = max(0, x1 - 100)
        expanded_y1 = max(0, y1 - 100)
        expanded_x2 = min(vid.shape[1], x2 + 100)
        expanded_y2 = min(vid.shape[0], y2 + 100)
        cv2.rectangle(vid, (expanded_x1, expanded_y1), (expanded_x2, expanded_y2), (255, 0, 0), 2)
    
    face_path = os.path.join(CACHE_DIR, 'temp.jpg')
    cv2.imwrite(face_path, vid)

    return center_face, vid

def facial_recognition(video_frame, rectangle, frames, count):
    rectangle2, processed_frame = detect_bounding_box(video_frame)

    if rectangle2:
        if rectangle is None or not is_stable_rectangle(rectangle, rectangle2):
            rectangle = rectangle2
            frames = 0
            print("New rectangle detected, resetting frames to 0")
        else:
            frames += 1
            print(f"Stable rectangle detected, incrementing frames: {frames}")
    else:
        rectangle = None
        frames = 0
        print("No rectangle detected, resetting frames to 0")

    if frames >= 20 and rectangle:
        x1, y1, x2, y2 = rectangle
        face = video_frame[y1:y2, x1:x2]
        face_path = os.path.join(CACHE_DIR, 'face.jpg')
        cv2.imwrite(face_path, face)
        count += 1
        frames = 0

        base64_image = encode_image(face_path)
        chat_completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text",
                         "text": "Describe the person infront of you and their environment?"},

                        {"type": "image_url",
                         "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }
            ]
        )
        print(f"AI API Response: {chat_completion.choices[0].message.content}")

    return processed_frame, rectangle, frames, count

def is_stable_rectangle(old_rect, new_rect, tolerance=500): # High Tolerance on purpse, need to find sweet spot
    if old_rect is None or new_rect is None:
        return False
    ox1, oy1, ox2, oy2 = old_rect
    nx1, ny1, nx2, ny2 = new_rect
    return (
        abs(ox1 - nx1) < tolerance and
        abs(oy1 - ny1) < tolerance and
        abs(ox2 - nx2) < tolerance and
        abs(oy2 - ny2) < tolerance
    )

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
