# Usa una imagen base oficial de Python (es buena práctica fijar la versión)
FROM python:3.9-alpine

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

RUN apk add --no-cache build-base freetype-dev libpng-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:${PORT:-8000}"]