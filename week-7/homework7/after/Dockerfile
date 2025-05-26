# Stage 1: builder
FROM python:3.13-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: runtime
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
ENV PATH=/root/.local/bin:$PATH

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

RUN adduser --disabled-password --gecos "" appuser
USER appuser

HEALTHCHECK CMD curl --fail http://localhost:5000/ping?ip=127.0.0.1 || exit 1

CMD ["python3", "app.py"]
