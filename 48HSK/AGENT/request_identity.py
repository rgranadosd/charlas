"""Request-scoped caller identity for HTTP service invocations."""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any, Dict, Iterator, Optional


@dataclass(frozen=True)
class CallerIdentity:
    access_token: str
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


_current_caller_identity: ContextVar[Optional[CallerIdentity]] = ContextVar(
    "current_caller_identity",
    default=None,
)


def get_caller_identity() -> Optional[CallerIdentity]:
    return _current_caller_identity.get()


@contextmanager
def use_caller_identity(identity: Optional[CallerIdentity]) -> Iterator[None]:
    token = _current_caller_identity.set(identity)
    try:
        yield
    finally:
        _current_caller_identity.reset(token)