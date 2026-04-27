"""Optional OpenTelemetry bootstrap for the HTTP service mode."""

from __future__ import annotations

import os
from typing import Optional


def _bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def bootstrap_fastapi_observability(app, service_name: str) -> bool:
    """Instrument FastAPI and common HTTP clients when OTel dependencies are available."""
    if _bool_env("OTEL_SDK_DISABLED", False):
        return False

    if getattr(app.state, "otel_bootstrapped", False):
        return True

    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
        from opentelemetry.instrumentation.requests import RequestsInstrumentor
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
    except ImportError:
        return False

    provider = trace.get_tracer_provider()
    if not isinstance(provider, TracerProvider):
        resource = Resource.create(
            {
                "service.name": service_name,
                "service.version": os.getenv("AGENT_SERVICE_VERSION", app.version or "0.1.0"),
            }
        )
        provider = TracerProvider(resource=resource)
        provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
        trace.set_tracer_provider(provider)

    excluded_urls = os.getenv("OTEL_FASTAPI_EXCLUDED_URLS", "/health,/ready")
    FastAPIInstrumentor.instrument_app(app, tracer_provider=provider, excluded_urls=excluded_urls)

    try:
        RequestsInstrumentor().instrument(tracer_provider=provider)
    except Exception:
        pass

    try:
        HTTPXClientInstrumentor().instrument(tracer_provider=provider)
    except Exception:
        pass

    app.state.otel_bootstrapped = True
    return True


def get_current_trace_id() -> Optional[str]:
    try:
        from opentelemetry import trace
    except ImportError:
        return None

    span = trace.get_current_span()
    if span is None:
        return None

    context = span.get_span_context()
    if not context or not context.is_valid:
        return None

    return f"{context.trace_id:032x}"


__all__ = ["bootstrap_fastapi_observability", "get_current_trace_id"]
