import numpy as np
import cv2
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from ultralytics import YOLO
import requests

# Инициализация приложения и модели
app = FastAPI()
model = YOLO("yolov5s.pt")  # Пример модели YOLO

# Настройка логгирования
logging.basicConfig(level=logging.INFO)


class HealthCheckResponse(BaseModel):
    status: str
    details: str = None


@app.post("/inference")
async def inference(file: UploadFile = File(...)):
    """
    Обрабатывает POST-запрос для инференса изображения.

    Параметры:
        file (UploadFile): Изображение, загружаемое пользователем в виде файла.

    Возвращает:
        dict: Словарь, содержащий результаты инференса в виде координат и вероятностей обнаруженных объектов.

    Процесс:
    - Считывает изображение из запроса и преобразует его в массив numpy.
    - Запускает модель YOLO для предсказания объектов на изображении.
    - Преобразует результаты в читаемый словарь и возвращает их в ответе.
    """
    try:
        # Валидация файла
        if file.content_type not in ["image/jpeg", "image/png"]:
            logging.warning("Unsupported file format: %s", file.content_type)
            raise HTTPException(status_code=400, detail="Unsupported file format")

        # Преобразование изображения для инференса
        image = np.frombuffer(await file.read(), np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image data")

        # Инференс и преобразование результатов
        results = model.predict(image)
        predictions = results.pandas().xyxy[0].to_dict(orient="records")
        logging.info("Inference completed successfully")
        return {"prediction": predictions}

    except Exception as e:
        logging.error("Inference error: %s", str(e))
        raise HTTPException(status_code=500, detail="Inference error")


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Проверяет состояние сервиса и зависимостей.

    Возвращает:
        dict: Словарь со статусом состояния сервиса и его зависимостей.

    Процесс:
    - Отправляет запросы к сервисам Runner и Orchestrator для проверки их доступности.
    - Если оба сервиса активны, возвращает статус "ok".
    - В случае ошибки возвращает статус "error" с подробностями ошибки.
    """
    try:
        runner_response = requests.get("http://runner:8001/health")
        orchestrator_response = requests.get("http://orchestrator:8002/health")
        if runner_response.status_code == 200 and orchestrator_response.status_code == 200:
            logging.info("Health check passed")
            return {"status": "ok"}
    except Exception as e:
        logging.error("Health check failed: %s", str(e))
        return {"status": "error", "details": str(e)}
