import os
import shutil
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CPCTELERA_HOME = PROJECT_ROOT / "tools" / "cpctelera" / "cpctelera"
GENERATED_PROJECTS = PROJECT_ROOT / "generated_projects"
CPCT_MKPROJECT = CPCTELERA_HOME / "tools" / "scripts" / "cpct_mkproject"
IDSK = CPCTELERA_HOME / "tools" / "iDSK-0.13" / "bin" / "iDSK"
LOADER_TEMPLATE = (
    PROJECT_ROOT / "tools" / "cpctelera" / "examples" / "games" / "platformClimber" / "assets" / "dsk_files" / "PCLIMBER.BAS"
)
BLANK_SCREEN_SIZE = 16 * 1024
DEFAULT_PROJECT_NAME = "latestcp"


def sanitize_project_name(raw_name: str | None) -> str:
    candidate = (raw_name or "").strip().lower()
    sanitized = "".join(ch for ch in candidate if ch.isalnum())
    sanitized = sanitized[:8]
    return sanitized or DEFAULT_PROJECT_NAME


def _build_env() -> dict[str, str]:
    env = os.environ.copy()
    scripts_dir = str(CPCT_MKPROJECT.parent)
    env["CPCT_PATH"] = str(CPCTELERA_HOME)
    env["PATH"] = f"{scripts_dir}:{env.get('PATH', '')}" if env.get("PATH") else scripts_dir
    return env


def _sync_generated_sources(source_path: Path | None, target_path: Path) -> None:
    if not source_path or not source_path.exists():
        return

    if source_path.resolve() == target_path.resolve():
        return

    ignored_names = {
        "obj", ".git", ".DS_Store", "__pycache__", ".vscode", "tools", "vendor"
    }
    ignored_suffixes = {
        ".cdt", ".dsk", ".bin", ".ihx", ".lk", ".map", ".noi", ".rel", ".sym", ".lst",
        ".asm", ".rst"
    }

    for child in source_path.iterdir():
        if child.name in ignored_names:
            continue
        if child.is_file() and child.suffix.lower() in ignored_suffixes:
            continue

        destination = target_path / child.name
        if child.is_dir():
            shutil.copytree(child, destination, dirs_exist_ok=True)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(child, destination)


def _prepare_project(project_path: str | None) -> tuple[str, Path, Path | None]:
    source_path = Path(project_path).resolve() if project_path else None
    requested_name = source_path.name if source_path else DEFAULT_PROJECT_NAME
    project_name = sanitize_project_name(requested_name)
    target_path = GENERATED_PROJECTS / project_name
    return project_name, target_path, source_path


def _is_valid_cpct_scaffold(project_dir: Path) -> bool:
    return (
        project_dir.exists()
        and project_dir.is_dir()
        and (project_dir / "src").is_dir()
        and (project_dir / "src" / "main.c").is_file()
        and (project_dir / "cfg").is_dir()
        and (project_dir / "cfg" / "build_config.mk").is_file()
        and (project_dir / "Makefile").is_file()
    )


def _build_output(
    success: bool,
    return_code: int,
    stdout: str,
    stderr: str,
    artifacts: list[str] | None = None,
    build_notes: str = "",
) -> dict:
    return {
        "success": success,
        "return_code": return_code,
        "stdout": stdout,
        "stderr": stderr,
        "artifacts": artifacts or [],
        "build_notes": build_notes,
    }


def _inject_disk_loader(target_path: Path, project_name: str, env: dict[str, str]) -> str:
    dsk_path = target_path / f"{project_name}.dsk"
    if not dsk_path.exists() or not IDSK.exists() or not LOADER_TEMPLATE.exists():
        return ""

    loader_dir = target_path / "dsk_files"
    loader_dir.mkdir(parents=True, exist_ok=True)

    disc_path = loader_dir / "DISC.BAS"
    screen_path = loader_dir / "SCREEN.SCR"
    game_path = loader_dir / "GAME.BIN"
    export_dir = target_path / "obj" / "loader_tmp"

    try:
        shutil.copy2(LOADER_TEMPLATE, disc_path)
        screen_path.write_bytes(bytes(BLANK_SCREEN_SIZE))

        if export_dir.exists():
            shutil.rmtree(export_dir)
        export_dir.mkdir(parents=True, exist_ok=True)

        exported_name = f"{project_name.upper()}.BIN"
        subprocess.run(
            [str(IDSK), str(dsk_path), "-g", exported_name],
            cwd=str(export_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=120,
            env=env,
            check=True,
        )
        shutil.copy2(export_dir / exported_name, game_path)

        for command in (
            [str(IDSK), str(dsk_path), "-i", str(disc_path), "-f"],
            [str(IDSK), str(dsk_path), "-i", str(screen_path), "-c", "C000", "-e", "C000", "-t", "1", "-f"],
            [str(IDSK), str(dsk_path), "-i", str(game_path), "-f"],
        ):
            subprocess.run(
                command,
                cwd=str(target_path),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=120,
                env=env,
                check=True,
            )

        return "Added DISC.BAS, SCREEN.SCR, and GAME.BIN to the DSK for direct BASIC loading."
    except (OSError, subprocess.SubprocessError) as exc:
        return f"Loader injection failed: {exc}"
    finally:
        shutil.rmtree(export_dir, ignore_errors=True)


def run(project_path: str | None) -> tuple[dict, str]:
    project_name, target_path, source_path = _prepare_project(project_path)
    env = _build_env()

    if not CPCT_MKPROJECT.exists():
        return _build_output(
            success=False,
            return_code=-1,
            stdout="",
            stderr=f"cpct_mkproject not found at {CPCT_MKPROJECT}",
            build_notes="CPCtelera command-line tools are not available in the configured installation.",
        ), str(target_path)

    GENERATED_PROJECTS.mkdir(parents=True, exist_ok=True)

    try:
        if target_path.exists() and (not source_path or source_path.resolve() != target_path.resolve()):
            shutil.rmtree(target_path)

        if not target_path.exists():
            create_result = subprocess.run(
                [str(CPCT_MKPROJECT), project_name],
                cwd=str(GENERATED_PROJECTS),
                capture_output=True,
                text=True,
                timeout=120,
                env=env,
                check=True,
            )
        else:
            create_result = None

        _sync_generated_sources(source_path, target_path)

        if not _is_valid_cpct_scaffold(target_path):
            return _build_output(
                success=False,
                return_code=-1,
                stdout="",
                stderr=f"Invalid CPCtelera scaffold at {target_path}",
                build_notes=(
                    "Build skipped because the target project does not contain a valid "
                    "CPCtelera scaffold (src/, src/main.c, cfg/, cfg/build_config.mk, Makefile)."
                ),
            ), str(target_path)

        subprocess.run(
            ["make", "clean"],
            cwd=str(target_path),
            capture_output=True,
            text=True,
            timeout=120,
            env=env,
            check=False,
        )

        result = subprocess.run(
            ["make"],
            cwd=str(target_path),
            capture_output=True,
            text=True,
            timeout=300,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return _build_output(
            success=False,
            return_code=-1,
            stdout="",
            stderr="Build timed out after 300 seconds.",
            build_notes="Build timed out.",
        ), str(target_path)
    except subprocess.CalledProcessError as exc:
        return _build_output(
            success=False,
            return_code=exc.returncode,
            stdout=(exc.stdout or "")[-4000:],
            stderr=(exc.stderr or "")[-4000:],
            build_notes=f"cpct_mkproject failed while creating {project_name} in {GENERATED_PROJECTS}.",
        ), str(target_path)
    except FileNotFoundError:
        return _build_output(
            success=False,
            return_code=-1,
            stdout="",
            stderr="'make' not found. Install Xcode Command Line Tools: xcode-select --install",
            build_notes="make not available in PATH.",
        ), str(target_path)

    expected_cdt = target_path / f"{project_name}.cdt"
    expected_dsk = target_path / f"{project_name}.dsk"
    artifacts_ok = expected_cdt.exists() and expected_dsk.exists()
    success = result.returncode == 0 and artifacts_ok

    loader_note = ""
    if success:
        loader_note = _inject_disk_loader(target_path, project_name, env)

    artifacts = []
    for ext in ("*.dsk", "*.cdt", "*.bin", "*.sna"):
        artifacts += [str(p.relative_to(target_path)) for p in target_path.rglob(ext)]

    create_stdout = create_result.stdout[-2000:] if create_result and create_result.stdout else ""
    create_stderr = create_result.stderr[-2000:] if create_result and create_result.stderr else ""

    full_stdout = "\n".join(
        part for part in [create_stdout, result.stdout[-4000:] if result.stdout else ""] if part
    )
    full_stderr = "\n".join(
        part for part in [create_stderr, result.stderr[-4000:] if result.stderr else ""] if part
    )

    if success:
        notes = f"Build completed successfully in {target_path}."
        if artifacts:
            notes += f" Produced: {', '.join(artifacts)}."
        if loader_note:
            notes += f" {loader_note}"
    else:
        if result.returncode == 0 and not artifacts_ok:
            notes = (
                f"Build finished but expected artifacts were not found: "
                f"{expected_cdt.name}, {expected_dsk.name}."
            )
        else:
            notes = f"Build failed with exit code {result.returncode}."

    return _build_output(
        success=success,
        return_code=result.returncode,
        stdout=full_stdout,
        stderr=full_stderr,
        artifacts=artifacts,
        build_notes=notes,
    ), str(target_path)
