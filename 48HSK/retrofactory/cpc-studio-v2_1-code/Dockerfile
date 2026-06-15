FROM python:3.12-slim

# sdcc   — Z80 C compiler used by CPCtelera's Makefile
# g++    — needed to compile iDSK and hex2bin from source
# make   — build system for both CPCtelera projects and the tools themselves
RUN apt-get update && apt-get install -y --no-install-recommends \
        sdcc \
        g++ \
        make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first — separate layer so it's only rebuilt when
# requirements.txt changes, not on every code change.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Pre-download the RAG embedding model so it is baked into the image
# (no runtime fetch, which would depend on HuggingFace reachability).
RUN python -c "from fastembed import TextEmbedding; TextEmbedding(model_name='BAAI/bge-small-en-v1.5')"

COPY . .

# Compile iDSK and hex2bin only when cpctelera source is present in the repo.
# The orchestrator image is built from the same Dockerfile but doesn't include
# the cpctelera subtree, so these steps are safely skipped.
RUN if [ -d "cpctelera/cpctelera/tools/iDSK-0.13" ]; then \
      make -C cpctelera/cpctelera/tools/iDSK-0.13 \
       && make -C cpctelera/cpctelera/tools/hex2bin-2.0; \
    fi

RUN if [ -d "cpctelera/cpctelera/tools/sdcc-3.6.8-r9946/bin" ]; then \
      cd cpctelera/cpctelera/tools/sdcc-3.6.8-r9946/bin \
       && rm -f * \
       && for t in sdcc sdasz80 sdar sdcpp sdld sdldz80; do \
              p="$(which "$t" 2>/dev/null)"; \
              [ -n "$p" ] && ln -s "$p" "$t"; \
          done; \
    fi

# OTEL auto-instrumentation baked into the image (replaces the fragile
# custom-otel-init container that was lost on every component re-render).
# AMP_OTEL_ENDPOINT / AMP_AGENT_API_KEY are still injected by the
# instrumentation trait at deploy time; sitecustomize.py auto-loads via PYTHONPATH.
RUN pip install --no-cache-dir --target /otel-custom \
        opentelemetry-sdk opentelemetry-exporter-otlp-proto-http \
        opentelemetry-instrumentation-fastapi opentelemetry-instrumentation-asgi
COPY otel/sitecustomize.py /otel-custom/sitecustomize.py
ENV PYTHONPATH=/otel-custom

# Ensure the outputs directory exists so the pipeline can write to it at runtime
RUN mkdir -p scene_agent/outputs \
 && useradd -m -u 1000 appuser \
 && chown -R appuser:appuser /app
USER appuser

ENV CPCT_PATH=/app/cpctelera/cpctelera

EXPOSE 8000

CMD ["python", "main.py"]
