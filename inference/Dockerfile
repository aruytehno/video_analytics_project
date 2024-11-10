# Используйте подходящий базовый образ
FROM python:3.9-slim

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файл с зависимостями в контейнер
COPY requirements.txt .

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте код приложения в контейнер
COPY . .

# Запустите приложение
CMD ["python", "inference.py"]
