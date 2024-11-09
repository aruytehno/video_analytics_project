# Ваш базовый образ
FROM python:3.9

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копирование и запуск вашего приложения
COPY . /app
WORKDIR /app
CMD ["python", "inference.py"]