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

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8010/health', timeout=3).read()" || exit 1

CMD ["python", "-m", "uvicorn", "service:app", "--app-dir", "/app", "--host", "0.0.0.0", "--port", "8010"]
