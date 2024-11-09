# Легковесный Python-образ
FROM python:3.9-slim

# Установка рабочей директории
WORKDIR /app

# Копирование requirements.txt и установка зависимостей
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копирование скрипта wait-for-it.sh и установка разрешений
COPY ../wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Копирование исходного кода приложения
COPY . .

# Запуск VideoRunner
CMD ["python", "runner.py"]
