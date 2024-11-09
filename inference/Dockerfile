# Легковесный Python-образ
FROM python:3.9-slim

# Установка необходимых системных библиотек
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование скрипта wait-for-it.sh и установка разрешений
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Копирование requirements.txt и установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копирование исходного кода приложения
COPY . /app

# Установка переменной окружения
ENV PYTHONPATH="/app"

# Запуск сервера Uvicorn
CMD ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "8000"]
