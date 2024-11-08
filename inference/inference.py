from fastapi import FastAPI, File, UploadFile
import random

app = FastAPI()

@app.post("/inference")
async def inference(file: UploadFile = File(...)):
    return {"prediction": random.choice(["object_A", "object_B", "object_C"])}
