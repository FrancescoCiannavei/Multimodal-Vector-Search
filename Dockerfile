FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY public/ public/

RUN useradd --create-home appuser
USER appuser

EXPOSE 8080

CMD ["fastapi", "run", "src/main.py", "--port", "8080"]
