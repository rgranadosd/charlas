import os
import re
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
AMSDOS_HEADER_SIZE = 0x80
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
    project_path: str = "",
    build_notes: str = "",
) -> dict:
    return {
        "success": success,
        "return_code": return_code,
        "stdout": stdout,
        "stderr": stderr,
        "artifacts": artifacts or [],
        "project_path": project_path,
        "build_notes": build_notes,
    }


def _make_basic_record(line_number: int, payload: bytes) -> bytes:
    record_length = 4 + len(payload)
    return (
        record_length.to_bytes(2, "little")
        + line_number.to_bytes(2, "little")
        + payload
    )


def _encode_basic_integer(value: int) -> bytes:
    if 0 <= value <= 10:
        return bytes((0x0E + value,))
    if 0 <= value <= 0xFF:
        return bytes((0x19, value))
    if 0 <= value <= 0xFFFF:
        return bytes((0x1A,)) + value.to_bytes(2, "little")
    raise ValueError(f"Cannot encode BASIC integer literal: {value}")


def _build_amsdos_binary(filename: str, payload: bytes, load_address: int, exec_address: int | None = None) -> bytes:
    stem, _, suffix = filename.upper().partition(".")
    header = bytearray(AMSDOS_HEADER_SIZE)
    header[0] = 0
    header[1:9] = stem[:8].ljust(8).encode("ascii")
    header[9:12] = suffix[:3].ljust(3).encode("ascii")
    header[18] = 2
    header[21:23] = load_address.to_bytes(2, "little")
    header[24:26] = len(payload).to_bytes(2, "little")
    header[26:28] = (exec_address if exec_address is not None else load_address).to_bytes(2, "little")
    header[64:66] = len(payload).to_bytes(2, "little")
    checksum = sum(header[:67]) & 0xFFFF
    header[67:69] = checksum.to_bytes(2, "little")
    return bytes(header) + payload


def _retarget_loader_template_for_disk(load_address: str | None = None, program_name: str | None = None, run_address: str | None = None) -> bytes:
    template = LOADER_TEMPLATE.read_bytes()
    header = bytearray(template[:AMSDOS_HEADER_SIZE])
    body = template[AMSDOS_HEADER_SIZE:]
    header[1:12] = b"DISC    BAS"
    memory_limit = None
    if load_address:
        memory_limit = max(int(load_address, 16) - 1, 0)
    program_basename = (program_name or "GAME")[:8].upper().encode()

    records: list[bytes] = []
    position = 0
    while position + 4 <= len(body):
        record_length = int.from_bytes(body[position:position + 2], "little")
        if record_length == 0:
            break

        line_number = int.from_bytes(body[position + 2:position + 4], "little")
        record = body[position:position + record_length]

        if line_number == 20 and memory_limit is not None:
            records.append(
                _make_basic_record(
                    15,
                    bytes((0xAA, 0x20)) + _encode_basic_integer(memory_limit) + bytes((0x00,)),
                )
            )
        if line_number == 30:
            records.append(record)
            position += record_length
            continue
        elif line_number == 40:
            position += record_length
            continue
        elif line_number == 70:
            # Use LOAD then CALL instead of RUN: RUN for binaries above HIMEM
            # goes through MC_BOOT_PROGRAM which resets AMSDOS to tape mode,
            # producing "Press PLAY then any key". LOAD respects the AMSDOS header
            # and CALL jumps directly to the execution address.
            record = _make_basic_record(
                70,
                bytes((0xA8, 0x20, 0x22))
                + program_basename
                + b".BIN"
                + bytes((0x22, 0x00)),
            )
            records.append(record)
            if run_address:
                records.append(
                    _make_basic_record(
                        75,
                        bytes((0x83, 0x20))
                        + _encode_basic_integer(int(run_address, 16))
                        + bytes((0x00,)),
                    )
                )
            position += record_length
            continue

        records.append(record)
        position += record_length

    payload = b"".join(records) + b"\x00\x00"

    header[0x18:0x1A] = len(payload).to_bytes(2, "little")
    header[0x40:0x42] = len(payload).to_bytes(2, "little")
    header[0x42] = 0
    header[0x43:0x45] = b"\x00\x00"
    checksum = sum(header[:67]) & 0xFFFF
    header[0x43:0x45] = checksum.to_bytes(2, "little")
    return bytes(header) + payload


def _read_binary_addresses(target_path: Path) -> tuple[str, str] | None:
    addresses_path = target_path / "obj" / "binaryAddresses.log"
    if not addresses_path.exists():
        return None

    text = addresses_path.read_text(encoding="utf-8", errors="ignore")
    load_match = re.search(r"Load Address\s*=\s*([0-9A-Fa-f]+)", text)
    run_match = re.search(r"Run\s+Address\s*=\s*([0-9A-Fa-f]+)", text)
    if not load_match or not run_match:
        return None

    return load_match.group(1).upper(), run_match.group(1).upper()


def _inject_disk_loader(target_path: Path, project_name: str, env: dict[str, str]) -> str:
    dsk_path = target_path / f"{project_name}.dsk"
    if not dsk_path.exists() or not IDSK.exists() or not LOADER_TEMPLATE.exists():
        return ""

    loader_dir = target_path / "dsk_files"
    loader_dir.mkdir(parents=True, exist_ok=True)

    disc_path = loader_dir / "DISC.BAS"
    stale_game_path = loader_dir / "GAME.BIN"
    game_binary_path = target_path / "obj" / f"{project_name}.bin"
    binary_addresses = _read_binary_addresses(target_path)

    try:
        # DISC.BAS must target disk files. Reusing the platformClimber template
        # verbatim leaves tape-prefixed filenames (!screen.scr / !game), which
        # reproduces the classic "Press PLAY then any key" failure on boot.
        disc_path.write_bytes(
            _retarget_loader_template_for_disk(
                binary_addresses[0] if binary_addresses else None,
                project_name,
                binary_addresses[1] if binary_addresses else None,
            )
        )
        if stale_game_path.exists():
            stale_game_path.unlink()

        subprocess.run(
            [str(IDSK), str(dsk_path), "-r", "GAME.BIN"],
            cwd=str(target_path),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=120,
            env=env,
            check=False,
        )
        subprocess.run(
            [str(IDSK), str(dsk_path), "-r", f"{project_name.upper()}.BIN"],
            cwd=str(target_path),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=120,
            env=env,
            check=False,
        )
        subprocess.run(
            [str(IDSK), str(dsk_path), "-r", "SCREEN.SCR"],
            cwd=str(target_path),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=120,
            env=env,
            check=False,
        )

        commands = [
            [str(IDSK), str(dsk_path), "-i", str(disc_path), "-f"],
        ]
        if game_binary_path.exists() and binary_addresses:
            commands.append(
                [
                    str(IDSK),
                    str(dsk_path),
                    "-i",
                    str(game_binary_path),
                    "-c",
                    binary_addresses[0],
                    "-e",
                    binary_addresses[1],
                    "-t",
                    "1",
                    "-f",
                ]
            )

        for command in commands:
            subprocess.run(
                command,
                cwd=str(target_path),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=120,
                env=env,
                check=True,
            )

        return "Added DISC.BAS and an AMSDOS game binary to the DSK for direct BASIC loading."
    except (OSError, subprocess.SubprocessError) as exc:
        return f"Loader injection failed: {exc}"


def run(project_path: str | None) -> tuple[dict, str]:
    project_name, target_path, source_path = _prepare_project(project_path)
    env = _build_env()

    if not CPCT_MKPROJECT.exists():
        return _build_output(
            success=False,
            return_code=-1,
            stdout="",
            stderr=f"cpct_mkproject not found at {CPCT_MKPROJECT}",
            project_path=str(target_path),
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
                project_path=str(target_path),
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
            project_path=str(target_path),
            build_notes="Build timed out.",
        ), str(target_path)
    except subprocess.CalledProcessError as exc:
        return _build_output(
            success=False,
            return_code=exc.returncode,
            stdout=(exc.stdout or "")[-4000:],
            stderr=(exc.stderr or "")[-4000:],
            project_path=str(target_path),
            build_notes=f"cpct_mkproject failed while creating {project_name} in {GENERATED_PROJECTS}.",
        ), str(target_path)
    except FileNotFoundError:
        return _build_output(
            success=False,
            return_code=-1,
            stdout="",
            stderr="'make' not found. Install Xcode Command Line Tools: xcode-select --install",
            project_path=str(target_path),
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
        project_path=str(target_path),
        build_notes=notes,
    ), str(target_path)
