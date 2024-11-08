import cv2
import requests
import time

class VideoRunner:
    def __init__(self, video_source="video.mp4", inference_url="http://inference:8003/inference"):
        self.video_source = video_source
        self.inference_url = inference_url

    def preprocess_frame(self, frame):
        # Изменение цветовой схемы с BGR на RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    def process_frame(self, frame):
        # Закодировать изображение в формат JPEG
        _, img_encoded = cv2.imencode('.jpg', frame)
        # Отправить изображение в сервис инференса
        response = requests.post(self.inference_url, files={"file": img_encoded.tobytes()})
        print("Inference response:", response.json())

    def run(self):
        # Открыть видеопоток
        cap = cv2.VideoCapture(self.video_source)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            # Предварительная обработка кадра
            frame = self.preprocess_frame(frame)
            # Отправка кадра на инференс
            self.process_frame(frame)
            # Пауза (можно настроить под требования проекта)
            time.sleep(0.1)
        # Освобождение ресурса видеопотока
        cap.release()
