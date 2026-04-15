# Stage 1
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# Stage 2
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY --from=builder /install /usr/local
COPY . .

CMD ["sh", "-c", "sleep 3 && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]