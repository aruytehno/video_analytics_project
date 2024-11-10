import cv2
import requests
import time
import logging

# Устанавливаем уровень логирования и создаем логгер для вывода информации.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoRunner:
    """
    Класс для обработки и анализа видео в реальном времени. `VideoRunner` загружает видеофайл,
    обрабатывает каждый кадр и отправляет его на сервис инференса для анализа.

    Атрибуты:
        video_source (str): Путь к видеофайлу, который будет обрабатываться. По умолчанию 'video.mp4'.
        inference_url (str): URL для сервиса инференса, на который отправляются кадры для анализа.
    """

    def __init__(self, video_source="video.mp4", inference_url="http://inference:8003/inference"):
        """
        Инициализирует VideoRunner с указанным источником видео и URL сервиса инференса.

        Параметры:
            video_source (str): Путь к видеофайлу. По умолчанию 'video.mp4'.
            inference_url (str): URL API сервиса инференса. По умолчанию 'http://inference:8003/inference'.
        """
        self.video_source = video_source
        self.inference_url = inference_url

    def preprocess_frame(self, frame):
        """
        Подготавливает кадр для инференса, конвертируя его в цветовое пространство RGB.

        Параметры:
            frame (numpy.ndarray): Кадр, полученный из видео.

        Возвращает:
            numpy.ndarray: Кадр, преобразованный в цветовое пространство RGB.
        """
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    def process_frame(self, frame):
        """
        Отправляет кадр на инференс-сервис для анализа и логирует результат.

        Параметры:
            frame (numpy.ndarray): Кадр, прошедший предварительную обработку.

        Исключения:
            requests.RequestException: Если при отправке запроса на инференс-сервис произошла ошибка.
        """
        # Кодирует изображение в формат JPEG перед отправкой
        _, img_encoded = cv2.imencode('.jpg', frame)
        try:
            # Отправка кадра на инференс-сервис через POST-запрос
            response = requests.post(self.inference_url, files={"file": img_encoded.tobytes()})
            logger.info("Inference response: %s", response.json())
        except requests.RequestException as e:
            logger.error("Ошибка отправки запроса инференсу: %s", e)

    def run(self):
        """
        Запускает цикл обработки видео: считывает кадры, отправляет их на инференс и обрабатывает результат.

        Процесс:
            - Открывает видеофайл.
            - Читает и обрабатывает каждый кадр.
            - После завершения видео или ошибки освобождает ресурсы.

        Исключения:
            - Логирует ошибку, если не удалось открыть видеоисточник.
            - Прерывает цикл обработки, если достигнут конец видео.
        """
        # Открывает видеоисточник
        cap = cv2.VideoCapture(self.video_source)
        if not cap.isOpened():
            logger.error("Не удалось открыть видеоисточник")
            return

        while cap.isOpened():
            # Чтение кадра
            ret, frame = cap.read()
            if not ret:
                logger.info("Конец видео")
                break

            # Предобработка кадра и отправка на инференс
            frame = self.preprocess_frame(frame)
            self.process_frame(frame)

            # Устанавливаем интервал между обработкой кадров для контроля нагрузки на систему
            time.sleep(0.1)

        # Освобождаем ресурсы
        cap.release()
