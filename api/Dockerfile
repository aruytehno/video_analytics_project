# Используем легкий образ Python
FROM python:3.9-alpine

# Устанавливаем необходимые системные зависимости
RUN apk update && apk add --no-cache \
    libgl1-mesa-glx \
    libstdc++ \
    && rm -rf /var/cache/apk/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем все файлы приложения
COPY ./api /app
COPY ./orchestrator /app/orchestrator
COPY ./runner /app/runner
COPY ./requirements.txt /app/requirements.txt

# Устанавливаем зависимости одним RUN слоем
RUN pip install --no-cache-dir -r /app/requirements.txt

# Устанавливаем переменную окружения PYTHONPATH
ENV PYTHONPATH="/app:/app/orchestrator"

# Запускаем приложение с Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
