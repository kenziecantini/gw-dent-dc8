FROM python:3.13-alpine

RUN adduser -D appuser

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

USER appuser

HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost:5000/ || exit 1

CMD ["python", "app.py"]


