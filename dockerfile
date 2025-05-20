FROM python:3.12-slim

WORKDIR /app

# Instala dependencias del sistema necesarias para Node.js y npm
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Previene escribir archivos pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Previene buffering 'stdout' y 'stderr'
ENV PYTHONUNBUFFERED=1

# Copiar requirements.txt
COPY app/backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Exponer puertos para Django y React
EXPOSE 8000 3000

# No copiamos el código aquí, usaremos un volumen
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


