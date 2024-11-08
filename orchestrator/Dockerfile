# Используем легковесный Python-образ
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем содержимое директории orchestrator в контейнер
COPY . .

# Устанавливаем зависимости, если есть requirements.txt
RUN pip install -r requirements.txt

# Запускаем скрипт orchestrator.py при старте контейнера
CMD ["python", "orchestrator.py"]
