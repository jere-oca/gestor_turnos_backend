FROM python:3.12-slim

RUN mkdir /app

WORKDIR /app

# Previene escribir archivos pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Previene buffering 'stdout' y 'stderr'
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


