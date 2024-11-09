# Используем slim-образ Python
FROM python:3.9-slim

# Установка необходимых системных библиотек
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем приложение и задаем рабочую директорию
COPY . /app
WORKDIR /app

# Устанавливаем переменную окружения PYTHONPATH
ENV PYTHONPATH="/app"

# Запуск с помощью Uvicorn для асинхронного сервера
CMD ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "8000"]
