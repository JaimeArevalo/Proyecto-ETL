FROM python:3.10-slim

WORKDIR /app

# Copiar los archivos de requisitos primero para aprovechar la caché de capas de Docker
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . .

# Crear directorios para datos
RUN mkdir -p data/input data/output

# Ejecutar el ejemplo por defecto cuando se inicia el contenedor
CMD ["python", "ejemplo_uso.py"]