# Используем легковесный Python-образ
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем содержимое директории inference в контейнер
COPY . .

# Устанавливаем зависимости, если есть requirements.txt
RUN pip install -r requirements.txt

# Запускаем скрипт inference.py при старте контейнера
CMD ["python", "inference.py"]
