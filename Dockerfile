# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create tables before seeding
RUN python -m app.create_db
RUN python -m app.seed

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]