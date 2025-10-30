# Базовый образ с Python
FROM python:3.11-slim

# Устанавливаем зависимости для Tkinter и GUI
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Копируем твой файл внутрь контейнера
WORKDIR /app
COPY main.py .

# Команда запуска GUI
CMD ["python", "main.py"]
