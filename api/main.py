from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Simple in-memory state
state = {"status": "inactive"}

class StateChange(BaseModel):
    new_state: str

@app.get("/scenario/{id}")
def get_scenario(id: int):
    return {"id": id, "status": state["status"]}

@app.post("/scenario/{id}/state")
def change_scenario_state(id: int, state_change: StateChange):
    if state_change.new_state not in ["init_startup", "active", "init_shutdown", "inactive"]:
        raise HTTPException(status_code=400, detail="Invalid state")
    state["status"] = state_change.new_state
    return {"id": id, "new_state": state["status"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}
