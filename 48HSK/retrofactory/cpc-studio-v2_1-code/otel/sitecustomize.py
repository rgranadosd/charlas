import os
import json
import base64
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("amp-otel-sitecustomize")

def _decode_jwt_payload(token):
    try:
        payload = token.split(".")[1]
        payload += "=" * (4 - len(payload) % 4)
        return json.loads(base64.b64decode(payload))
    except Exception:
        return {}

try:
  from opentelemetry import trace
  from opentelemetry.sdk.resources import Resource
  from opentelemetry.sdk.trace import TracerProvider
  from opentelemetry.sdk.trace.export import BatchSpanProcessor
  from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
  from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
  from fastapi import FastAPI
  from starlette.responses import Response

  api_key = (os.getenv("AMP_AGENT_API_KEY") or "").strip()
  _raw_ep = (os.getenv("AMP_OTEL_ENDPOINT") or "").rstrip("/")
  endpoint = f"{_raw_ep}/v1/traces" if _raw_ep else "http://opentelemetry-collector.openchoreo-observability-plane.svc.cluster.local:4318/v1/traces"

  if api_key:
    jwt_data = _decode_jwt_payload(api_key)
    component_uid  = jwt_data.get("component_uid")  or (os.getenv("OPENCHOREO_COMPONENT_UID") or "cpc-pm")
    component_name = jwt_data.get("sub") or component_uid
    environment_uid = jwt_data.get("environment_uid") or (os.getenv("OPENCHOREO_ENVIRONMENT_UID") or "default")
    project_uid    = jwt_data.get("project_uid")    or (os.getenv("OPENCHOREO_PROJECT_UID") or "retro-factory")

    logger.info("OTEL UIDs: component=%s env=%s project=%s", component_uid, environment_uid, project_uid)

    # Trace-label model name. AMP_GENAI_MODEL is not injected by the platform, so
    # fall back to the per-agent model vars each agent actually uses to pick its
    # LLM (ORCHESTRATOR_MODEL for the PM, DEVELOPER/AUDIO/QA_MODEL for workers)
    # before the hardcoded default — otherwise every span is mislabelled.
    model_name = (
        os.getenv("AMP_GENAI_MODEL")
        or os.getenv("GENAI_MODEL")
        or os.getenv("LLM_MODEL")
        or os.getenv("ORCHESTRATOR_MODEL")
        or os.getenv("DEVELOPER_MODEL")
        or os.getenv("AUDIO_MODEL")
        or os.getenv("QA_MODEL")
        or "MISTRAL/codestral-latest"
    ).strip()

    resource = Resource.create({
      "service.name": component_uid,
      "openchoreo.dev/component-uid": component_uid,
      "openchoreo.dev/environment-uid": environment_uid,
      "openchoreo.dev/project-uid": project_uid,
    })
    exporter = OTLPSpanExporter(endpoint=endpoint, headers={
      "x-amp-api-key": api_key,
      "x-user-component": component_uid,
      "x-user-environment": environment_uid,
      "x-user-project": project_uid,
    })
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer("amp.custom.chat")

    _orig_init = FastAPI.__init__

    def _patched_init(self, *args, **kwargs):
      _orig_init(self, *args, **kwargs)
      try:
        FastAPIInstrumentor.instrument_app(self)
      except Exception as ie:
        logger.exception("FastAPI instrumentation failed: %s", ie)

      @self.middleware("http")
      async def _amp_chat_span_middleware(request, call_next):
        if request.method == "POST" and request.url.path in ("/chat", "/run"):
          raw = await request.body()
          try:
            payload = json.loads(raw.decode("utf-8") or "{}")
          except Exception:
            payload = {}

          if request.url.path == "/chat":
            user_content = str(payload.get("message", ""))
            conversation_id = str(payload.get("session_id", ""))
          else:
            # /run — orchestrated task call from another agent (e.g. cpc-pm -> cpc-developer)
            conversation_id = str(
              payload.get("task_id")
              or payload.get("session_id")
              or payload.get("job_id")
              or ""
            )
            title = payload.get("title") or payload.get("goal") or ""
            description = payload.get("description") or ""
            project_name = payload.get("project_name") or ""
            parts = []
            if title:
              parts.append(f"[{title}]")
            if project_name:
              parts.append(f"project={project_name}")
            if description:
              parts.append(str(description))
            user_content = " ".join(parts) if parts else json.dumps(payload)[:2000]

          with tracer.start_as_current_span("chat") as span:
            span.set_attribute("gen_ai.operation.name", "chat")
            span.set_attribute("gen_ai.system", "custom")
            span.set_attribute("gen_ai.request.model", model_name)
            span.set_attribute("amp.model.name", model_name)
            # Use human-readable component name (JWT sub) so the observer can
            # classify this as SpanTypeAgent and populate agentData.Name.
            span.set_attribute("gen_ai.agent.name", component_name)
            # Force agent span classification — checked first in DetermineSpanType
            span.set_attribute("traceloop.span.kind", "agent")
            span.set_attribute("gen_ai.conversation.id", conversation_id)
            span.set_attribute("gen_ai.input.messages", json.dumps([{"role": "user", "content": user_content}]))
            response = await call_next(request)
            body = b""
            async for chunk in response.body_iterator:
              body += chunk
            text = ""
            in_tokens = None
            out_tokens = None
            tot_tokens = None
            try:
              out = json.loads(body.decode("utf-8") or "{}")
              text = str(out.get("response") or out.get("summary") or out.get("message") or out)
              in_tokens = out.get("input_tokens")
              out_tokens = out.get("output_tokens")
              tot_tokens = out.get("total_tokens")
            except Exception:
              text = body.decode("utf-8", errors="ignore")
            span.set_attribute("gen_ai.output.messages", json.dumps([{"role": "assistant", "content": text[:4000]}]))
            if isinstance(in_tokens, int):
              span.set_attribute("gen_ai.usage.input_tokens", in_tokens)
              span.set_attribute("gen_ai.usage.prompt_tokens", in_tokens)
            if isinstance(out_tokens, int):
              span.set_attribute("gen_ai.usage.output_tokens", out_tokens)
              span.set_attribute("gen_ai.usage.completion_tokens", out_tokens)
            if isinstance(tot_tokens, int):
              span.set_attribute("gen_ai.usage.total_tokens", tot_tokens)
            elif isinstance(in_tokens, int) and isinstance(out_tokens, int):
              span.set_attribute("gen_ai.usage.total_tokens", in_tokens + out_tokens)
            return Response(content=body, status_code=response.status_code, headers=dict(response.headers), media_type=response.media_type)
        return await call_next(request)

    FastAPI.__init__ = _patched_init
    logger.info("Custom OTEL + GenAI sitecustomize initialized (service.name=%s) -- capturing /chat and /run", component_uid)
  else:
    logger.warning("AMP_AGENT_API_KEY missing; tracing disabled")
except Exception as e:
  logger.exception("Custom OTEL init failed: %s", e)
