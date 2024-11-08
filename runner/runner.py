import cv2
import requests
import time

class VideoRunner:
    def __init__(self, video_source="video.mp4", inference_url="http://inference:8003/inference"):
        self.video_source = video_source
        self.inference_url = inference_url

    def process_frame(self, frame):
        _, img_encoded = cv2.imencode('.jpg', frame)
        response = requests.post(self.inference_url, files={"file": img_encoded.tobytes()})
        print("Inference response:", response.json())

    def run(self):
        cap = cv2.VideoCapture(self.video_source)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            self.process_frame(frame)
            time.sleep(0.1)  # simulate some delay
        cap.release()
