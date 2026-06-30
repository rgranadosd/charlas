FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY common common
COPY agents/qa agents/qa

RUN pip install --no-cache-dir --target /otel-custom \
        opentelemetry-sdk opentelemetry-exporter-otlp-proto-http \
        opentelemetry-instrumentation-fastapi opentelemetry-instrumentation-asgi
COPY otel/sitecustomize.py /otel-custom/sitecustomize.py

ENV PYTHONPATH=/otel-custom:/app/agents/qa:/app

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["python", "agents/qa/main.py"]
