FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    RUN_MODE=service \
    AGENT_ENV_PROFILE=service \
    SERVICE_HOST=0.0.0.0 \
    SERVICE_PORT=8010 \
    OTEL_SERVICE_NAME=rafa-agent \
    OTEL_RESOURCE_ATTRIBUTES=service.name=rafa-agent,deployment.environment=dev,agent.type=external \
    OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf

WORKDIR /app

COPY requirements-service.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements-service.txt \
    && python - <<'PY'
from pathlib import Path

handler = Path("/usr/local/lib/python3.12/site-packages/semantic_kernel/connectors/ai/open_ai/services/open_ai_handler.py")
text = handler.read_text()
old = '''from semantic_kernel.connectors.ai.open_ai import (
    OpenAIAudioToTextExecutionSettings,
    OpenAIChatPromptExecutionSettings,
    OpenAIEmbeddingPromptExecutionSettings,
    OpenAIPromptExecutionSettings,
    OpenAITextToAudioExecutionSettings,
    OpenAITextToImageExecutionSettings,
)'''
new = '''from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_audio_to_text_execution_settings import (
    OpenAIAudioToTextExecutionSettings,
)
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import (
    OpenAIChatPromptExecutionSettings,
    OpenAIEmbeddingPromptExecutionSettings,
    OpenAIPromptExecutionSettings,
)
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_text_to_audio_execution_settings import (
    OpenAITextToAudioExecutionSettings,
)
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_text_to_image_execution_settings import (
    OpenAITextToImageExecutionSettings,
)'''
if old not in text:
    raise SystemExit("semantic-kernel import block not found")
handler.write_text(text.replace(old, new, 1))

package_init = Path("/usr/local/lib/python3.12/site-packages/semantic_kernel/connectors/ai/open_ai/__init__.py")
package_init.write_text('''# Patched for service runtime: avoid eager Azure/realtime imports.\n\nfrom semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_audio_to_text_execution_settings import (\n    OpenAIAudioToTextExecutionSettings,\n)\nfrom semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import (\n    OpenAIChatPromptExecutionSettings,\n    OpenAIEmbeddingPromptExecutionSettings,\n    OpenAIPromptExecutionSettings,\n    OpenAITextPromptExecutionSettings,\n)\nfrom semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_text_to_audio_execution_settings import (\n    OpenAITextToAudioExecutionSettings,\n)\nfrom semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_text_to_image_execution_settings import (\n    OpenAITextToImageExecutionSettings,\n)\nfrom semantic_kernel.connectors.ai.open_ai.services.open_ai_audio_to_text import OpenAIAudioToText\nfrom semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion import OpenAIChatCompletion\nfrom semantic_kernel.connectors.ai.open_ai.services.open_ai_text_completion import OpenAITextCompletion\nfrom semantic_kernel.connectors.ai.open_ai.services.open_ai_text_embedding import OpenAITextEmbedding\nfrom semantic_kernel.connectors.ai.open_ai.services.open_ai_text_to_audio import OpenAITextToAudio\nfrom semantic_kernel.connectors.ai.open_ai.services.open_ai_text_to_image import OpenAITextToImage\nfrom semantic_kernel.connectors.ai.open_ai.settings.open_ai_settings import OpenAISettings\n\n__all__ = [\n    "OpenAIAudioToText",\n    "OpenAIAudioToTextExecutionSettings",\n    "OpenAIChatCompletion",\n    "OpenAIChatPromptExecutionSettings",\n    "OpenAIEmbeddingPromptExecutionSettings",\n    "OpenAIPromptExecutionSettings",\n    "OpenAISettings",\n    "OpenAITextCompletion",\n    "OpenAITextEmbedding",\n    "OpenAITextPromptExecutionSettings",\n    "OpenAITextToAudio",\n    "OpenAITextToAudioExecutionSettings",\n    "OpenAITextToImage",\n    "OpenAITextToImageExecutionSettings",\n]\n''')
PY

COPY . .

EXPOSE 8010

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8010/health', timeout=3).read()" || exit 1

CMD ["python", "-m", "uvicorn", "service:app", "--app-dir", "/app", "--host", "0.0.0.0", "--port", "8010"]
