# Легковесный Python-образ
FROM python:3.9-slim

# Установка рабочей директории
WORKDIR /app

# Копирование requirements.txt и установка зависимостей
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Копирование исходного кода приложения
COPY . .

# Запуск Orchestrator
CMD ["python", "orchestrator.py"]
