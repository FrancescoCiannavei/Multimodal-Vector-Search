FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8080

WORKDIR /app

COPY main.py .
COPY public/ public/

RUN useradd --create-home appuser
USER appuser

EXPOSE 8080

CMD ["python", "main.py"]
