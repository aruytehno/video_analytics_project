# Dockerfile для api
FROM python:3.9-slim

WORKDIR /app

# Копируем весь проект
COPY . /app

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Указываем PYTHONPATH, чтобы найти orchestrator
ENV PYTHONPATH=/app:$PYTHONPATH

CMD ["python", "main.py"]
