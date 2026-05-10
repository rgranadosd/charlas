import os
import time
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

BASE = Path(__file__).resolve().parents[2]
ENV_FILE = BASE / ".env"
load_dotenv(ENV_FILE)

PROMPTS = BASE / "prompts"

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

PLATFORM_CONTEXT = """
Target platform: Amstrad CPC 6128
CPU: Z80A 4 MHz
RAM: 128 KB
Framework: CPCtelera
Toolchain: SDCC + make + cpct_mkproject
Absolute priorities:
1. Smooth controls
2. Smooth sprite motion
3. Maximum visual quality within realistic budget
Reject ideas that harm control feel or motion smoothness.
""".strip()


def build_model() -> ChatOpenAI:
    if LLM_PROVIDER == "mistral":
        api_key = os.getenv("MISTRAL_API_KEY")
        model = os.getenv("MISTRAL_MODEL", "mistral-large-latest")
        base_url = os.getenv("MISTRAL_BASE_URL", "https://api.mistral.ai/v1")
        return ChatOpenAI(
            model=model,
            temperature=0.2,
            api_key=api_key,
            base_url=base_url,
        )

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    return ChatOpenAI(
        model=model,
        temperature=0.2,
        api_key=api_key,
    )


def load_prompt(name: str) -> str:
    return (PROMPTS / f"{name}.txt").read_text(encoding="utf-8")


def invoke_with_backoff(llm, messages, retries=5, base_delay=2):
    last_error = None
    for attempt in range(retries):
        try:
            return llm.invoke(messages)
        except Exception as e:
            last_error = e
            text = str(e).lower()
            retryable = "rate limit" in text or "429" in text or "rate_limited" in text
            if not retryable or attempt == retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"[retry] rate limit detectado, reintentando en {delay}s...")
            time.sleep(delay)
    raise last_error


def structured_call(prompt_name: str, schema, user_request: str, extra_context: str = ""):
    llm = build_model().with_structured_output(schema)
    system = load_prompt(prompt_name)
    context = PLATFORM_CONTEXT
    if extra_context:
        context += f"\n\nRetrieved project knowledge:\n{extra_context}"
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"{context}\n\nUser request:\n{user_request}"},
    ]
    return invoke_with_backoff(llm, messages)