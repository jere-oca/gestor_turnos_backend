FROM python:3.11-slim

WORKDIR /app/backend

RUN apt update && apt install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY entrypoint.sh .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

EXPOSE 8000

CMD ["/app/backend/entrypoint.sh"]
