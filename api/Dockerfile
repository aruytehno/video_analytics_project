# api/Dockerfile
FROM python:3.9-slim
WORKDIR /app

# Скопировать API файлы и orchestrator из корневой директории
COPY ./api /app
COPY ./orchestrator /app/orchestrator

# Установка зависимостей
RUN pip install -r /app/requirements.txt

# Установите переменную PYTHONPATH
ENV PYTHONPATH="/app:/app/orchestrator"

CMD ["python", "main.py"]
