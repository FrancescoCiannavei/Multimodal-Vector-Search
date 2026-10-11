FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# FFmpeg libraries for torchcodec, which decodes the audio and video files
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir torch torchvision torchcodec --index-url https://download.pytorch.org/whl/cpu

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY public/ public/

RUN useradd --create-home appuser
USER appuser

# Created as appuser so the model-cache volume mounted here is writable
RUN mkdir -p /home/appuser/.cache/huggingface

EXPOSE 8080

CMD ["fastapi", "run", "src/main.py", "--port", "8080"]
