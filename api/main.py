from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from orchestrator.orchestrator import Orchestrator

app = FastAPI()

# Создаем один экземпляр Orchestrator на уровне модуля, чтобы состояние сохранялось между запросами
orchestrator = Orchestrator()

class StateChange(BaseModel):
    new_state: str

@app.get("/scenario/{id}")
def get_scenario(id: int):
    # Возвращает текущее состояние orchestrator'а
    return {"id": id, "status": orchestrator.get_state(), "parameters": {"example_param": "value"}}

@app.post("/scenario/{id}/state")
def change_scenario_state(id: int, state_change: StateChange):
    # Проверяем корректность нового состояния
    if state_change.new_state not in Orchestrator.states:
        raise HTTPException(status_code=400, detail="Invalid state")

    # Меняем состояние через метод Orchestrator
    orchestrator.change_state(state_change.new_state)
    return {"id": id, "new_state": orchestrator.get_state()}

@app.get("/health")
def health_check():
    return {"status": "ok"}
