from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from orchestrator.orchestrator import Orchestrator

app = FastAPI()

# Создаем один экземпляр Orchestrator на уровне модуля, чтобы состояние сохранялось между запросами
orchestrator = Orchestrator()


class StateChange(BaseModel):
    """
    Модель данных для запроса изменения состояния.

    Поля:
        new_state (str): Новое состояние для Orchestrator.
    """
    new_state: str


@app.get("/scenario/{id}")
def get_scenario(id: int):
    """
    Получает текущий сценарий и его состояние.

    Параметры:
        id (int): Идентификатор сценария.

    Возвращает:
        dict: Словарь с идентификатором сценария, текущим состоянием и примером параметров.
    """
    return {"id": id, "status": orchestrator.get_state(), "parameters": {"example_param": "value"}}


@app.post("/scenario/{id}/state")
def change_scenario_state(id: int, state_change: StateChange):
    """
    Изменяет состояние сценария.

    Параметры:
        id (int): Идентификатор сценария.
        state_change (StateChange): Новый статус, который нужно установить.

    Возвращает:
        dict: Словарь с идентификатором сценария и обновленным состоянием.

    Исключения:
        HTTPException: Поднимается, если переданное состояние недопустимо.

    Описание:
    - Проверяет корректность нового состояния в Orchestrator.
    - Обновляет состояние через соответствующий метод Orchestrator.
    """
    if state_change.new_state not in Orchestrator.states:
        raise HTTPException(status_code=400, detail="Invalid state")

    orchestrator.change_state(state_change.new_state)
    return {"id": id, "new_state": orchestrator.get_state()}


@app.get("/health")
def health_check():
    """
    Проверка состояния API.

    Возвращает:
        dict: Сообщение о состоянии API (статус 'ok', если API работает корректно).
    """
    return {"status": "ok"}
