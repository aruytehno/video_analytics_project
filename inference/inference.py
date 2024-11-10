import numpy as np
from fastapi import FastAPI, File, UploadFile
import requests
from ultralytics import YOLO

app = FastAPI()
model = YOLO("yolov5s.pt")  # пример модели YOLO


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
    image = np.frombuffer(await file.read(), np.uint8)
    results = model.predict(image)
    return {"prediction": results.pandas().xyxy[0].to_dict(orient="records")}


@app.get("/health")
def health_check():
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
            return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "details": str(e)}
