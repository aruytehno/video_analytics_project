import numpy as np
from fastapi import FastAPI, File, UploadFile
import requests
from ultralytics import YOLO

app = FastAPI()
model = YOLO("yolov5s.pt")  # пример модели YOLO

@app.post("/inference")
async def inference(file: UploadFile = File(...)):
    # Чтение изображения из запроса и преобразование в нужный формат
    image = np.frombuffer(await file.read(), np.uint8)
    results = model.predict(image)
    return {"prediction": results.pandas().xyxy[0].to_dict(orient="records")}

@app.get("/health")
def health_check():
    try:
        # Пример проверки состояния Runner'а и Orchestrator'а
        runner_response = requests.get("http://runner:8001/health")
        orchestrator_response = requests.get("http://orchestrator:8002/health")
        if runner_response.status_code == 200 and orchestrator_response.status_code == 200:
            return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "details": str(e)}
