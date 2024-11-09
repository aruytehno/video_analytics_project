import cv2
import requests
import time
import logging

# Настройка логгирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
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
        logger.info(f"VideoRunner инициализирован с video_source={video_source} и inference_url={inference_url}")

    def preprocess_frame(self, frame):
        """
        Подготавливает кадр для инференса, конвертируя его в цветовое пространство RGB.

        Параметры:
            frame (numpy.ndarray): Кадр, полученный из видео.

        Возвращает:
            numpy.ndarray: Кадр, преобразованный в цветовое пространство RGB.
        """
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

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
            response.raise_for_status()
            result = response.json()
            logger.info("Инференс успешен: %s", result)
        except requests.RequestException as e:
            logger.error("Ошибка при отправке запроса на инференс-сервис: %s", e)
        except ValueError:
            logger.error("Некорректный ответ от сервиса инференса (ожидался JSON)")

    def run(self):
        """
        Запускает цикл обработки видео: считывает кадры и отправляет их на инференс.
        """
        # Открывает видеоисточник
        cap = cv2.VideoCapture(self.video_source)
        if not cap.isOpened():
            logger.error("Не удалось открыть видеоисточник")
            return

        logger.info("Начало обработки видео")
        while cap.isOpened():
            # Чтение кадра
            ret, frame = cap.read()
            if not ret:
                logger.info("Конец видео")
                break

            try:
                frame = self.preprocess_frame(frame)
                self.process_frame(frame)
                time.sleep(0.1)
            except Exception as e:
                logger.error("Ошибка при обработке кадра: %s", e)
                break

        # Освобождаем ресурсы
        cap.release()
        logger.info("Видеообработка завершена")
