"""Build Agent — FastAPI server that compiles a CPCtelera project for real.

This is the deterministic counterpart to the LLM agents: it has the full
CPCtelera SDK + sdcc baked into the image, so it can actually run `make` and
return real compiler errors. The pipeline's fix loop calls it instead of trying
(and failing) to compile inside cpc-pm, which ships without the SDK.

Endpoint: POST /compile
  body:    { "files": [ {"path": "src/main.c", "content": "..."}, ... ] }
  returns: { "ok": bool, "errors": str, "dsk_base64": str|null }
"""
from __future__ import annotations

import base64
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="CPC Studio — Build Agent")

# Baked into the image (see Dockerfile.build)
_SDK      = Path(os.environ.get("CPCT_PATH", "/app/cpctelera/cpctelera"))
_TEMPLATE = Path(os.environ.get("CPC_TEMPLATE", "/app/pruebacpct"))  # Makefile + cfg/


class FileSpec(BaseModel):
    path: str
    content: str


class CompileRequest(BaseModel):
    files: list[FileSpec]


class CompileResult(BaseModel):
    ok: bool
    errors: str = ""
    dsk_base64: str | None = None


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


def _scaffold(run_dir: Path) -> None:
    """Replicate scene_agent.build_and_run._scaffold inside the build image."""
    (run_dir / "src").mkdir(parents=True, exist_ok=True)
    (run_dir / "obj").mkdir(parents=True, exist_ok=True)
    shutil.copy(_TEMPLATE / "Makefile", run_dir / "Makefile")
    cfg_dst = run_dir / "cfg"
    if cfg_dst.exists():
        shutil.rmtree(cfg_dst)
    shutil.copytree(_TEMPLATE / "cfg", cfg_dst)

    cfg_mk = cfg_dst / "build_config.mk"
    if cfg_mk.exists():
        src = cfg_mk.read_text(encoding="utf-8")
        src = re.sub(r"^(PROJNAME\s*:=\s*)\S+", r"\1scene", src, flags=re.MULTILINE)
        src = re.sub(r"^(CPCT_PATH\s*:=\s*).*", rf"\1{_SDK.resolve()}", src, flags=re.MULTILINE)
        cfg_mk.write_text(src, encoding="utf-8")


@app.post("/compile", response_model=CompileResult)
def compile_project(req: CompileRequest) -> CompileResult:
    with tempfile.TemporaryDirectory(prefix="cpcbuild_") as tmp:
        run_dir = Path(tmp)
        _scaffold(run_dir)

        # Only source files are accepted; everything else is ignored for safety.
        for f in req.files:
            rel = f.path.lstrip("/")
            if ".." in rel or not (rel.startswith("src/") or rel == "Makefile"):
                continue
            target = run_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f.content, encoding="utf-8")

        env = {**os.environ, "CPCT_PATH": str(_SDK.resolve())}
        try:
            result = subprocess.run(
                ["make", "-C", str(run_dir)],
                capture_output=True, text=True, errors="replace", env=env, timeout=180,
            )
        except subprocess.TimeoutExpired:
            return CompileResult(ok=False, errors="make timed out after 180s")

        if result.returncode != 0:
            errors = (result.stderr + result.stdout)[-4000:]
            return CompileResult(ok=False, errors=errors)

        dsk = next(run_dir.glob("*.dsk"), None)
        dsk_b64 = base64.b64encode(dsk.read_bytes()).decode() if dsk else None
        return CompileResult(ok=True, errors="", dsk_base64=dsk_b64)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
