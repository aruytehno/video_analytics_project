import cv2
import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoRunner:
    def __init__(self, video_source="video.mp4", inference_url="http://inference:8003/inference"):
        self.video_source = video_source
        self.inference_url = inference_url

    def preprocess_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    def process_frame(self, frame):
        _, img_encoded = cv2.imencode('.jpg', frame)
        try:
            response = requests.post(self.inference_url, files={"file": img_encoded.tobytes()})
            logger.info("Inference response: %s", response.json())
        except requests.RequestException as e:
            logger.error("Ошибка отправки запроса инференсу: %s", e)

    def run(self):
        cap = cv2.VideoCapture(self.video_source)
        if not cap.isOpened():
            print("Не удалось открыть видеоисточник")
            return
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Конец видео")
                break
            frame = self.preprocess_frame(frame)
            self.process_frame(frame)
            time.sleep(0.1)
        cap.release()
