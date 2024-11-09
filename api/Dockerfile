FROM python:3.9-slim

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*


# Остальная часть Dockerfile остается неизменной
WORKDIR /app
COPY . /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
ENV PYTHONPATH="/app:/app/orchestrator"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
