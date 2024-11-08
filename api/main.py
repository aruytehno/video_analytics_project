from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from orchestrator.orchestrator import Orchestrator

app = FastAPI()

# Simple in-memory state
state = {"status": "inactive"}

class StateChange(BaseModel):
    new_state: str

@app.get("/scenario/{id}")
def get_scenario(id: int):
    return {"id": id, "status": state["status"], "parameters": {"example_param": "value"}}

@app.post("/scenario/{id}/state")
def change_scenario_state(id: int, state_change: StateChange):
    if state_change.new_state not in ["init_startup", "in_startup_processing", "active", "init_shutdown", "in_shutdown_processing", "inactive"]:
        raise HTTPException(status_code=400, detail="Invalid state")
    # Здесь важно обновить стейт-машину orchestrator'а
    orchestrator = Orchestrator()
    orchestrator.change_state(state_change.new_state)
    return {"id": id, "new_state": orchestrator.get_state()}


@app.get("/health")
def health_check():
    return {"status": "ok"}
