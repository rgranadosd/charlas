FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    RUN_MODE=service \
    AGENT_ENV_PROFILE=service \
    SERVICE_HOST=0.0.0.0 \
    SERVICE_PORT=8010

WORKDIR /app

COPY requirements-service.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements-service.txt

COPY . .

EXPOSE 8010

CMD ["python", "main.py"]
