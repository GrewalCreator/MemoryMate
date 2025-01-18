import time

import cv2
import requests
from picamera2 import Picamera2

API_URL = (
    "https://3c0c-2607-fea8-e3a1-ca00-993d-ad2c-ebba-a23d.ngrok-free.app/api/live-feed"
)
IMAGE_INTERVAL = 1.0


def capture_image(picam2):
    """
    Captures an image from the camera and returns it as JPEG bytes.
    """
    frame = picam2.capture_array()
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    ret, buffer = cv2.imencode(".jpg", frame_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    if not ret:
        raise ValueError("Failed to encode image to JPEG")

    image_bytes = buffer.tobytes()
    return image_bytes


def send_image(image_bytes):
    """
    Sends the image bytes to the server via an HTTP POST request.
    """
    files = {"video": ("frame.jpg", image_bytes, "image/jpeg")}

    data = {"distance": 12}

    try:
        response = requests.post(API_URL, files=files, data=data, timeout=10)
        response.raise_for_status()
        print(
            f"Image sent successfully. Server responded with status code {response.status_code}"
        )
    except requests.exceptions.Timeout:
        print("POST request timed out.")
    except requests.exceptions.ConnectionError:
        print("Connection error occurred.")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send image: {e}")


def main():
    picam2 = Picamera2()
    picam2.configure(picam2.create_still_configuration())
    picam2.start()
    print("Camera started.")

    try:
        while True:
            start_time = time.time()

            image_bytes = capture_image(picam2)
            print("Image captured.")

            send_image(image_bytes)

            elapsed_time = time.time() - start_time
            sleep_time = max(0, IMAGE_INTERVAL - elapsed_time)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("Interrupted by user.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        picam2.stop()
        print("Camera stopped.")


if __name__ == "__main__":
    main()
