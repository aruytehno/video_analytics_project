# Используем легковесный Python-образ
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем содержимое директории api в контейнер
COPY . .

# Устанавливаем зависимости, если есть requirements.txt
RUN pip install -r requirements.txt

# Запускаем скрипт main.py при старте контейнера
CMD ["python", "main.py"]
