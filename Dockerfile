# Imagen base oficial de Python
FROM python:3.12-slim

# Evitar que Python escriba archivos .pyc y buffering de stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /ztrack_mongodb

# Copiar e instalar dependencias primero (mejor uso de caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Puerto por defecto
EXPOSE 8033

# Ejecutar la aplicación FastAPI
# Usar uvicorn directamente (sin reload en producción)
CMD ["uvicorn", "app.server.app:app", "--host", "0.0.0.0", "--port", "8033"]
