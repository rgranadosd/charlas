import re
from pathlib import PurePosixPath
from typing import Any

_C_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_TYPE_HINT_RE = re.compile(r"\b(?:void|u8|u16|u32|i8|i16|i32|char|int|short|long|bool)\b")

_DECL_RE = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_\s\*]*?)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*;\s*$",
    re.MULTILINE,
)
_DEF_RE = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_\s\*]*?)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*\{",
    re.MULTILINE,
)

_BAD_FUSED_FN_AND_TYPE_RE = re.compile(
    r"\b([A-Za-z_][A-Za-z0-9_]*)(?:u8|u16|u32|i8|i16|i32|char|int|short|long|bool)\s+[A-Za-z_][A-Za-z0-9_]*(?:\s*,|\s*;)",
    re.IGNORECASE,
)
_BAD_INCLUDE_CONCAT_RE = re.compile(r"#\s*include\s+[\"<][^\n\">]*\.hinclude", re.IGNORECASE)
_TYPED_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_\*\s]*\s+[A-Za-z_][A-Za-z0-9_]*$")


def _normalize_storage_qualifier(value: str) -> str:
    token = _compact_spaces(value)
    if not token:
        raise ValueError("Empty storage qualifier")
    if not all(_C_IDENT_RE.fullmatch(part) for part in token.split(" ")):
        raise ValueError(f"Invalid storage qualifier: {value}")
    return token


def _compact_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", str(value).strip())


def _line_number(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def _normalize_identifier(name: str) -> str:
    token = _compact_spaces(name)
    if not _C_IDENT_RE.fullmatch(token):
        raise ValueError(f"Invalid C identifier: {name}")
    return token


def _normalize_c_type(type_name: str) -> str:
    token = _compact_spaces(type_name)
    token = re.sub(r"\s*\*\s*", "*", token)
    if not token:
        raise ValueError("C type cannot be empty")
    return token


def _normalize_param(param: Any) -> str:
    if isinstance(param, dict):
        raw_type = str(param.get("type", "")).strip()
        raw_name = str(param.get("name", "")).strip()
    elif isinstance(param, (tuple, list)) and len(param) == 2:
        raw_type = str(param[0]).strip()
        raw_name = str(param[1]).strip()
    else:
        token = _compact_spaces(str(param))
        if token.lower() == "void":
            return "void"

        match = re.match(r"^(.*?)\s+([A-Za-z_][A-Za-z0-9_]*)$", token)
        if not match:
            raise ValueError(f"Invalid C parameter: {param}")
        raw_type = match.group(1).strip()
        raw_name = match.group(2).strip()

    if not raw_type or not raw_name:
        raise ValueError(f"Invalid C parameter: {param}")

    return f"{_normalize_c_type(raw_type)} {_normalize_identifier(raw_name)}"


def _render_params(params: list[Any] | tuple[Any, ...] | None) -> str:
    values = list(params or [])
    if not values:
        return "void"

    normalized = [_normalize_param(value) for value in values]
    if len(normalized) > 1 and "void" in normalized:
        raise ValueError('Invalid params: "void" must be the only parameter')
    return "void" if normalized == ["void"] else ", ".join(normalized)


def render_c_function_decl(return_type: str, name: str, params: list[Any] | tuple[Any, ...] | None) -> str:
    rendered_return = _normalize_c_type(return_type)
    rendered_name = _normalize_identifier(name)
    rendered_params = _render_params(params)
    return f"{rendered_return} {rendered_name}({rendered_params});"


def render_c_function_def(
    return_type: str,
    name: str,
    params: list[Any] | tuple[Any, ...] | None,
    body_lines: list[str] | None = None,
) -> str:
    signature = render_c_function_decl(return_type, name, params).rstrip(";")
    lines = list(body_lines or [])
    if not lines:
        return f"{signature} {{\n}}\n"

    body = "\n".join((f"    {line}" if line else "") for line in lines)
    return f"{signature} {{\n{body}\n}}\n"


def render_c_include(header: str) -> str:
    token = str(header).strip()
    if not token:
        raise ValueError("Header include cannot be empty")

    if token.startswith("#include"):
        token = token.replace("#include", "", 1).strip()

    if token.startswith("<") and token.endswith(">"):
        value = token[1:-1].strip()
        if not value.endswith(".h"):
            raise ValueError(f"Invalid system header include: {header}")
        return f"#include <{value}>"

    value = token.strip('"').replace("\\", "/")
    if value.startswith("./"):
        value = value[2:]
    if value.startswith("src/"):
        value = value[4:]

    value = PurePosixPath(value).as_posix()
    if not value or ".." in PurePosixPath(value).parts or not value.endswith(".h"):
        raise ValueError(f"Invalid local header include: {header}")

    return f"#include \"{value}\""


def render_c_struct(name: str, fields: list[Any] | tuple[Any, ...]) -> str:
    struct_name = _normalize_identifier(name)
    rendered_fields: list[str] = []

    for field in list(fields or []):
        if isinstance(field, dict):
            field_type = str(field.get("type", "")).strip()
            field_name = str(field.get("name", "")).strip()
        elif isinstance(field, (tuple, list)) and len(field) == 2:
            field_type = str(field[0]).strip()
            field_name = str(field[1]).strip()
        else:
            token = _compact_spaces(str(field)).rstrip(";")
            match = re.match(r"^(.*?)\s+([A-Za-z_][A-Za-z0-9_]*)$", token)
            if not match:
                raise ValueError(f"Invalid struct field: {field}")
            field_type = match.group(1).strip()
            field_name = match.group(2).strip()

        if not field_type or not field_name:
            raise ValueError(f"Invalid struct field: {field}")

        rendered_fields.append(f"{_normalize_c_type(field_type)} {_normalize_identifier(field_name)};")

    if not rendered_fields:
        rendered_fields = ["u8 _reserved;"]

    body = "\n".join(f"    {line}" for line in rendered_fields)
    return f"typedef struct {{\n{body}\n}} {struct_name};"


def _normalize_array_value(value: Any) -> str:
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, int):
        return str(value)

    token = _compact_spaces(str(value)).rstrip(",")
    if not token:
        raise ValueError("Array value cannot be empty")
    return token


def render_c_array_decl(
    type_name: str,
    name: str,
    values: list[Any] | tuple[Any, ...] | None,
    qualifiers: list[str] | tuple[str, ...] | None = None,
) -> str:
    rendered_type = _normalize_c_type(type_name)
    rendered_name = _normalize_identifier(name)

    rendered_qualifiers = [_normalize_storage_qualifier(item) for item in list(qualifiers or []) if str(item).strip()]
    head = " ".join(rendered_qualifiers + [rendered_type]).strip()

    if values is None:
        return f"{head} {rendered_name}[];"

    rendered_values = [_normalize_array_value(item) for item in list(values)]
    payload = ", ".join(rendered_values) if rendered_values else "0"
    return f"{head} {rendered_name}[] = {{ {payload} }};"


def render_c_const_array(type_name: str, name: str, values: list[Any] | tuple[Any, ...]) -> str:
    return render_c_array_decl(type_name, name, values, qualifiers=["const"])


def _normalize_signature(return_type: str, name: str, params_block: str) -> str | None:
    try:
        normalized_return = _normalize_c_type(return_type)
        normalized_name = _normalize_identifier(name)
    except ValueError:
        return None

    params_raw = _compact_spaces(params_block)
    if not params_raw or params_raw == "void":
        params = "void"
    else:
        parts = [item.strip() for item in params_raw.split(",") if item.strip()]
        if not parts:
            params = "void"
        else:
            try:
                params = ", ".join(_normalize_param(part) for part in parts)
            except ValueError:
                return None

    return f"{normalized_return} {normalized_name}({params})"


def _collect_header_declarations(content: str) -> dict[str, str]:
    declarations: dict[str, str] = {}
    for match in _DECL_RE.finditer(content):
        signature = _normalize_signature(match.group(1), match.group(2), match.group(3))
        if signature:
            declarations[match.group(2)] = signature
    return declarations


def _collect_source_definitions(content: str) -> dict[str, str]:
    definitions: dict[str, str] = {}
    for match in _DEF_RE.finditer(content):
        signature = _normalize_signature(match.group(1), match.group(2), match.group(3))
        if signature:
            definitions[match.group(2)] = signature
    return definitions


def _looks_like_broken_prototype_without_parentheses(line: str) -> bool:
    token = _compact_spaces(line).rstrip(";")
    if not token:
        return False
    if "(" in token or ")" in token:
        return False

    parts = [item.strip() for item in token.split(",") if item.strip()]
    if len(parts) < 2:
        return False

    if any("{" in part or "}" in part or "[" in part or "]" in part for part in parts):
        return False

    typed_parts = [part for part in parts if _TYPED_IDENTIFIER_RE.fullmatch(part)]
    if len(typed_parts) < 2:
        return False

    first_tokens = parts[0].split()
    if not first_tokens:
        return False

    first_type = first_tokens[0].strip("*")
    if _TYPE_HINT_RE.search(first_type):
        # Valid variable declarations like "u8 a, b, c;" should not be flagged.
        return False

    later_has_known_type = False
    for part in parts[1:]:
        tokens = part.split()
        if not tokens:
            continue
        if _TYPE_HINT_RE.search(tokens[0].strip("*")):
            later_has_known_type = True
            break

    return later_has_known_type


def detect_c_generation_issues(files: dict[str, str]) -> list[str]:
    issues: list[str] = []

    for path in sorted(files.keys()):
        content = str(files.get(path, ""))

        for match in _BAD_FUSED_FN_AND_TYPE_RE.finditer(content):
            line = _line_number(content, match.start())
            issues.append(
                f"{path}:{line}: suspicious fused function/type token near '{match.group(0).strip()}'."
            )

        for match in _BAD_INCLUDE_CONCAT_RE.finditer(content):
            line = _line_number(content, match.start())
            issues.append(
                f"{path}:{line}: invalid include concatenation '{match.group(0).strip()}'."
            )

        in_struct_block = False
        struct_brace_depth = 0

        for line_num, raw_line in enumerate(content.splitlines(), start=1):
            line = raw_line.strip()

            if "typedef struct" in line:
                in_struct_block = True
                struct_brace_depth += line.count("{") - line.count("}")
                continue

            if in_struct_block:
                struct_brace_depth += line.count("{") - line.count("}")
                if struct_brace_depth <= 0 and "}" in line and line.endswith(";"):
                    in_struct_block = False
                    struct_brace_depth = 0
                continue

            if not line or line.startswith("#") or "(" in line or ")" in line:
                continue
            if not line.endswith(";") or "," not in line:
                continue
            if not _looks_like_broken_prototype_without_parentheses(line):
                continue
            issues.append(
                f"{path}:{line_num}: prototype-like line without valid parentheses '{line}'."
            )

    src_files = {path: str(content) for path, content in files.items() if str(path).endswith(".c")}
    header_files = {path: str(content) for path, content in files.items() if str(path).endswith(".h")}

    for src_path, src_content in sorted(src_files.items()):
        header_path = str(PurePosixPath(src_path).with_suffix(".h"))
        if header_path not in header_files:
            continue

        header_decls = _collect_header_declarations(header_files[header_path])
        source_defs = _collect_source_definitions(src_content)

        for name in sorted(set(header_decls.keys()) & set(source_defs.keys())):
            if header_decls[name] == source_defs[name]:
                continue
            issues.append(
                f"{src_path}: signature mismatch for '{name}' between {header_path} and {src_path}."
            )

    return list(dict.fromkeys(issues))