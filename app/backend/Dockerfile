FROM python:3.11-slim

WORKDIR /app/backend

RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY entrypoint.sh .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

EXPOSE 8000

CMD ["/app/backend/entrypoint.sh"]
