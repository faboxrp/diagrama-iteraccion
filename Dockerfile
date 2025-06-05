FROM python:3.11-slim-bullseye

# Variables de entorno para optimizar
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1

RUN python -m pip install --upgrade pip

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Comando para ejecutar la aplicación
CMD ["sh", "-c", "gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:${PORT:-8000}"]