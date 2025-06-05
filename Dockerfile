# Usa una imagen base oficial de Python
FROM python:alpine

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación al directorio de trabajo
COPY . .

# El puerto en el que Uvicorn/Gunicorn se ejecutará dentro del contenedor.
# EXPOSE 8000 

# Comando para ejecutar la aplicación.
# Usamos Gunicorn para gestionar los workers de Uvicorn en producción.
# El comando `sh -c` permite la sustitución de variables de entorno.
CMD ["sh", "-c", "gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:${PORT:-8000}"]