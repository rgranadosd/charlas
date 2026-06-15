FROM python:3.12-slim

WORKDIR /app

# Only this service carries the heavy embedding engine (onnxruntime + model).
RUN pip install --no-cache-dir fastapi==0.115.0 uvicorn==0.30.6 pydantic==2.9.2 fastembed==0.8.0
# Bake the model so there is no runtime HuggingFace fetch.
RUN python -c "from fastembed import TextEmbedding; TextEmbedding(model_name='BAAI/bge-small-en-v1.5')"

COPY agents/embed/main.py main.py

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["python", "main.py"]
