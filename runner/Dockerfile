# Используем легковесный Python-образ
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем содержимое директории runner в контейнер
COPY . .

# Устанавливаем зависимости, если есть requirements.txt
RUN pip install -r requirements.txt

# Запускаем скрипт runner.py при старте контейнера
CMD ["python", "runner.py"]
