FROM python:3.12-slim

WORKDIR /app

# Previene escribir archivos pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Previene buffering 'stdout' y 'stderr'
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# No copiamos el código aquí, usaremos un volumen
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


