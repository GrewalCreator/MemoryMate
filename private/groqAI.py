import os
import cv2
from dotenv import load_dotenv
import numpy as np
import base64
from groq import Groq

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(BASE_DIR, "..", ".env")
load_dotenv(dotenv_path="./.env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in the environment variables. Ensure .env is correctly configured.")

# Load the Haar cascade classifier for face detection
face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Function to detect faces and draw bounding boxes
def detect_bounding_box(vid, rectangle, frames):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))

    # Find the face closest to the center
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
            center_face = (x, y, w, h)

    if center_face:
        x, y, w, h = center_face
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
        if is_new_rectangle(rectangle, faces):
            rectangle = (x - 100, y - 100, x + w + 100, y + h + 100)
        cv2.rectangle(vid, (rectangle[0], rectangle[1]), (rectangle[2], rectangle[3]), (255, 0, 0), 4)
        font_color = (255, 255, 255) if frames < 20 else (0, 0, 255)
        cv2.putText(vid, f"Frames: {frames}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, font_color, 2, cv2.LINE_AA)
    return faces, rectangle

# Function to check if the detected rectangle is new
def is_new_rectangle(old_rectangle, faces):
    if old_rectangle is None:
        return True

    old_x, old_y, old_w, old_h = old_rectangle[0], old_rectangle[1], old_rectangle[2] - old_rectangle[0], old_rectangle[3] - old_rectangle[1]
    for (new_x, new_y, new_w, new_h) in faces:
        if new_x >= old_x and new_y >= old_y and (new_x + new_w) <= (old_x + old_w) and (new_y + new_h) <= (old_y + old_h):
            return False

    return True

# Function to encode the image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Main facial recognition loop
def facial_recognition(video_frame):
    rectangle = None
    frames = 0
    count = 0

    # Process the video frame
    faces, rectangle2 = detect_bounding_box(video_frame, rectangle, frames)
    if rectangle2 != rectangle:
        rectangle = rectangle2
        frames = 0
    else:
        frames += 1

    # Save the detected face if present for 20+ frames
    if frames > 20 and rectangle:
        x, y, w, h = rectangle
        face = video_frame[y:h, x:w]
        face_path = f"face_{count}.jpg"
        cv2.imwrite(face_path, face)
        count += 1
        frames = 0

        # Encode the face image and send it to Groq API
        base64_image = encode_image(face_path)

        client = Groq(GROQ_API_KEY)
        chat_completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What's in this image?"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],
                }
            ]
        )

        print(chat_completion.choices[0].message.content)

    return video_frame