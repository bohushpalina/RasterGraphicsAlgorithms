FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    python3-tk \
    tk \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY main.py .

CMD ["python", "main.py"]
