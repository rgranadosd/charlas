"""Pre-build C code guard — catches invented API calls before SDCC runs.

Checks src/main.c for:
  - Forbidden stdlib/non-existent CPCtelera functions (hard errors → abort build)
  - Unknown cpct_* calls not in the known CPCtelera API (warnings only)
  - Missing required boilerplate
"""
from __future__ import annotations

import re
from typing import NamedTuple

_G  = "\033[32m"
_Y  = "\033[33m"
_R  = "\033[31m"
_B  = "\033[1m"
_RS = "\033[0m"


class GuardResult(NamedTuple):
    ok: bool
    errors: list[str]
    warnings: list[str]


# Functions that do NOT exist and will always cause link/compiler failure.
_FORBIDDEN: frozenset[str] = frozenset({
    # Invented cpct_* functions — common model hallucinations
    "cpct_sprintf", "cpct_printf", "cpct_itoa", "cpct_atoi",
    "cpct_strcpy",  "cpct_strcat", "cpct_strlen", "cpct_strcmp",
    "cpct_strncpy", "cpct_strncmp",
    "cpct_init",              # does not exist — use cpct_disableFirmware()
    "cpct_drawHexWordM0",     # does not exist — extract digits manually
    "cpct_drawHexByteM0",     # does not exist
    "cpct_drawCharM0",        # does not exist — use cpct_drawStringM0 with char buf[2]
    "cpct_setPaletteFromGIMP", # does not exist
    # AKP sound system — requires pre-compiled tracker data; model always gets types wrong
    "cpct_akp_SFXPlay", "cpct_akp_SFXStop", "cpct_akp_SFXInit",
    "cpct_akp_MusicPlay", "cpct_akp_MusicStop", "cpct_akp_MusicInit",
    "cpct_akp_Init", "cpct_akp_Update",
    # Wrong key constant names — correct: Key_Space, Key_CursorLeft, Key_CursorRight
    "KEY_Space", "KEY_CursorLeft", "KEY_CursorRight", "KEY_Return", "KEY_Escape",
    "CPCT_KEY_Space", "CPCT_KEY_CursorLeft", "CPCT_KEY_CursorRight",
    # C stdlib — not available (no stdio.h / stdlib.h / string.h)
    "sprintf", "printf", "fprintf", "scanf", "sscanf",
    "strlen", "strcpy", "strcat", "strcmp", "strncpy",
    "malloc", "free", "calloc", "realloc",
    "puts", "gets", "fopen", "fclose", "fread", "fwrite",
    "itoa", "atoi", "atof", "atol",
})

# CPCtelera public API subset used by this project — anything outside
# this set gets a warning (not a hard error).
_KNOWN_CPCT: frozenset[str] = frozenset({
    "cpct_disableFirmware", "cpct_enableFirmware",
    "cpct_setVideoMode", "cpct_setBorder", "cpct_setStackSize",
    "cpct_setPalette", "cpct_fw2hw",
    "cpct_setPALColour",                          # preferred per-pen palette init
    "cpct_px2byteM0", "cpct_px2byteM1",           # correct colour-byte generation
    "cpct_getScreenPtr",
    "cpct_drawSolidBox", "cpct_drawSprite", "cpct_drawTile",
    "cpct_drawStringM0", "cpct_drawStringM1", "cpct_drawStringM2",
    "cpct_clearScreen", "cpct_clearScreenBox",    # preferred screen clear
    "cpct_memset", "cpct_memset_f8", "cpct_memset_f64",
    "cpct_isKeyPressed", "cpct_scanKeyboard", "cpct_scanKeyboard_f", "cpct_scanKeyboardAll",
    "cpct_waitVSYNC", "cpct_waitHSYNC",
    "cpct_hflipSpriteM0", "cpct_hflipSpriteM1",
})


# ---------------------------------------------------------------------------
# C89 declaration-after-statement hoisting helpers
# ---------------------------------------------------------------------------

# Matches a simple variable declaration WITHOUT a function-call initializer:
#   u8 i, j;       u8 i;       i8 ball_x, ball_y;       u8* pvmem;
#   u8 arr[N];     u8 x = 0;   (but NOT  u8* p = cpct_getScreenPtr(...); )
_HOIST_DECL_RE = re.compile(
    r"^\s*"
    r"(?:u8|i8|u16|i16|u32|i32|char|int|unsigned(?:\s+\w+)?|signed(?:\s+\w+)?)"
    r"\s*\*?\s*"
    r"\w+(?:\s*\[\s*\w*\s*\])*"
    r"(?:\s*,\s*\*?\s*\w+(?:\s*\[\s*\w*\s*\])*)*"
    r"(?:\s*=\s*[^(;,\n]+)?"   # optional initializer — but no '(' (= no function call)
    r"\s*;",
)
_IS_COMMENT_OR_PP = re.compile(r"^\s*(?://|/\*|\*/|\*|#)")


def _is_hoist_candidate(line: str) -> bool:
    """True iff line looks like a simple C89 variable declaration with no function call."""
    s = line.strip()
    if not s or not s.endswith(";"):
        return False
    if _IS_COMMENT_OR_PP.match(line):
        return False
    if not _HOIST_DECL_RE.match(line):
        return False
    # Reject if there's a '(' in the initializer portion — function call
    eq = s.find("=")
    if eq != -1 and "(" in s[eq:]:
        return False
    return True


def _hoist_block_declarations(block_lines: list) -> list:
    """Within a function block, move simple declarations that come after the first
    non-declaration statement to the top of the block (C89 compliance).

    Only operates on lines at depth 0 of the given block (i.e., the function's direct
    scope — not inside nested if/for/while/switch bodies).
    """
    depth = 0
    first_stmt_idx = None      # index of first non-declaration line
    late_decl_indices = []     # indices of declarations that appear AFTER first_stmt_idx

    for idx, line in enumerate(block_lines):
        s = line.strip()
        opens  = s.count("{")
        closes = s.count("}")
        at_depth_zero = (depth == 0)
        depth = max(0, depth + opens - closes)

        if not s or _IS_COMMENT_OR_PP.match(line):
            continue  # blank / comment — ignore for ordering purposes

        if at_depth_zero:
            if _is_hoist_candidate(line):
                if first_stmt_idx is not None:
                    late_decl_indices.append(idx)
            else:
                if first_stmt_idx is None:
                    first_stmt_idx = idx

    if not late_decl_indices or first_stmt_idx is None:
        return block_lines  # nothing to fix

    decl_set = set(late_decl_indices)
    extracted = [block_lines[i] for i in late_decl_indices]
    result = []
    inserted = False
    for idx, line in enumerate(block_lines):
        if idx in decl_set:
            continue
        if idx == first_stmt_idx and not inserted:
            result.extend(extracted)
            inserted = True
        result.append(line)
    return result


def _hoist_block_recursive(lines: list) -> list:
    """Walk lines; for every {…} block found, hoist its depth-0 declarations then recurse
    into nested blocks — so declarations inside if/for/while bodies are also fixed."""
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        opens = s.count("{")
        closes = s.count("}")

        if opens > closes:
            result.append(line)
            i += 1
            depth = opens - closes
            body: list = []
            while i < len(lines):
                l = lines[i]
                ss = l.strip()
                o = ss.count("{")
                c = ss.count("}")
                depth += o - c
                if depth <= 0:
                    hoisted = _hoist_block_declarations(body)
                    result.extend(_hoist_block_recursive(hoisted))
                    result.append(l)
                    i += 1
                    break
                body.append(l)
                i += 1
            continue

        result.append(line)
        i += 1

    return result


def _hoist_c89_declarations(code: str) -> str:
    """Post-process generated C: hoist variable declarations above the first statement
    in every brace-delimited block (including nested if/for/while bodies) to satisfy
    C89 requirements."""
    lines = code.splitlines(keepends=True)
    return "".join(_hoist_block_recursive(lines))


# Matches global variable declarations with non-compile-time-constant initializers.
# e.g.  u8 ball_x = paddle_x + 5;   → strips to  u8 ball_x;
# Fires when the initializer contains arithmetic operators with identifiers OR function calls.
# Only applied at file scope (before any function body opens).
_GLOBAL_NONCONST_INIT_RE = re.compile(
    r"^([ \t]*(?:u8|i8|u16|i16|u32|i32|char|int|unsigned(?:\s+char)?)\s*\*?\s*\w+(?:\s*\[\s*\w*\s*\])*)"
    r"\s*=\s*"
    r"(?=[^;]*(?:[+\-\*\/]|>>|<<|\()[^;]*;)"  # lookahead: expression with op or function call
    r"([^;]+);",
    re.MULTILINE,
)


def _strip_nonconstant_global_inits(code: str) -> str:
    """Remove initializers from global declarations that are not compile-time constants.

    'Initializer element is not a compile-time constant' (SDCC error 2) fires when a
    global variable is initialized with an expression involving other variables or function
    calls. SDCC requires global initializers to be pure literals or #define constants.

    Only processes lines BEFORE the first function body (file/global scope).
    """
    lines = code.splitlines(keepends=True)
    result = []
    in_function = False
    brace_depth = 0

    for line in lines:
        s = line.strip()
        # Track when we enter the first function body
        opens  = s.count("{")
        closes = s.count("}")
        if opens > closes and not in_function:
            in_function = True

        if not in_function:
            # At file scope: strip non-constant initializers
            m = _GLOBAL_NONCONST_INIT_RE.match(line)
            if m:
                declaration = m.group(1)
                initializer_expr = m.group(2).strip()
                # Take only the first value (before any comma in multi-var declarations)
                first_val = initializer_expr.split(',')[0].strip()
                # Strip if: function call present
                has_call = '(' in first_val
                # Strip if: lowercase variable used as operand (e.g. paddle_x + 5)
                # Pattern: lowercase_id followed or preceded by arithmetic op
                has_var_operand = bool(
                    re.search(r'\b[a-z][a-z0-9_]*\b\s*[+\-\*/]', first_val) or
                    re.search(r'[+\-\*/]\s*\b[a-z][a-z0-9_]*\b', first_val)
                )
                if has_call or has_var_operand:
                    line = declaration.rstrip() + ";\n"

        brace_depth += opens - closes
        result.append(line)

    return "".join(result)


# ---------------------------------------------------------------------------
# Public auto-fix entry point
# ---------------------------------------------------------------------------

# Matches: TYPE *?VAR = func_or_expr(...);  — declaration with a function-call initializer.
# These are valid C89 only at the very top of a block. When they appear after a statement
# (or inside a nested for/while body after other code) SDCC rejects them with
# "syntax error: token -> 'u8'".
# Fix: split into bare declaration + assignment so the hoisting pass can move it up.
_SPLIT_DECL_CALL_RE = re.compile(
    r"^([ \t]*)"
    r"((?:u8|i8|u16|i16|u32|i32|char|int|unsigned(?:\s+char)?|signed(?:\s+char)?)"
    r"\s*\*?\s*)"
    r"(\w+)"
    r"\s*=\s*"
    r"(\w[^;]*\([^;]*\)[^;]*)"   # initializer that contains a function call
    r"\s*;",
    re.MULTILINE,
)


def _split_funcall_decls(code: str) -> str:
    """Split 'TYPE *VAR = func(...);' into 'TYPE *VAR;\\nVAR = func(...);' everywhere.

    After splitting, the bare 'TYPE *VAR;' is a simple declaration that the
    hoisting pass can move to the top of the enclosing function body.
    Inside nested for/while bodies the bare declaration is valid C89 as long as
    it stays at the start of that block.
    """
    def _replacer(m: re.Match) -> str:
        indent, type_part, name, init = m.group(1), m.group(2), m.group(3), m.group(4)
        return f"{indent}{type_part}{name};\n{indent}{name} = {init.strip()};"
    return _SPLIT_DECL_CALL_RE.sub(_replacer, code)


# Detects ball_y bottom-clamp patterns that prevent the floor check from firing.
# Examples the model generates:
#   if (ball_vy > 0) { ball_y++; if (ball_y >= 200-BALL_H) { ball_y=200-BALL_H; ball_vy=-1; }}
#   if (ball_y >= FLOOR_Y - BALL_H) { ball_y = FLOOR_Y - BALL_H; ball_vy = -1; }
# These clamp ball_y so the floor check `ball_y + BALL_H - 1 >= FLOOR_Y` never fires.
# Fix: remove the inner clamp block, leaving only ball_y++.
_BALL_Y_CLAMP_RE = re.compile(
    r"(ball_y\+\+\s*;)\s*"
    r"if\s*\(\s*ball_y\s*>=\s*[^)]+\)\s*\{"
    r"[^}]*ball_y\s*=\s*[^;]+;\s*"
    r"[^}]*ball_vy\s*=\s*-1\s*;"
    r"[^}]*"   # allow extra code inside block (e.g. audio_play_sfx)
    r"\}",
    re.DOTALL,
)


def _remove_ball_y_clamp(code: str) -> str:
    """Remove bottom y-clamp patterns that prevent the floor check from firing."""
    return _BALL_Y_CLAMP_RE.sub(r"\1", code)


def _fix_hud_positions(code: str) -> str:
    """Enforce exact HUD getScreenPtr positions for LIVES: and SCORE labels/digits.

    Required layout:
      "LIVES:" label  → x=0  (drawn once in init_game)
      lives digit     → x=24 (drawn in draw_lives)
      "SCORE" label   → x=40 (drawn once in init_game)
      score digits    → x=64 (drawn in draw_score)
    """
    # Fix getScreenPtr x-coordinate for the line immediately before drawStringM0 with given literal
    def _fix_label(src: str, label: str, correct_x: int) -> str:
        # Matches:  pv = cpct_getScreenPtr(CPCT_VMEM_START, <X>, 0);
        #           cpct_drawStringM0("<label>",  pv,  ...);
        pat = re.compile(
            r'(pv\s*=\s*cpct_getScreenPtr\s*\(\s*CPCT_VMEM_START\s*,\s*)(\d+)(\s*,\s*0\s*\)\s*;'
            r'\s*\n\s*cpct_drawStringM0\s*\(\s*"' + re.escape(label) + r'")',
            re.MULTILINE,
        )
        return pat.sub(lambda m: m.group(1) + str(correct_x) + m.group(3), src)

    code = _fix_label(code, "LIVES:", 0)
    code = _fix_label(code, "LIVES",  0)   # also fix if model omitted colon
    code = _fix_label(code, "SCORE",  40)
    code = _fix_label(code, "SCORE:", 40)   # also fix if model added colon to SCORE
    # Normalise SCORE: → SCORE (no colon)
    code = re.sub(r'cpct_drawStringM0\s*\(\s*"SCORE:"', 'cpct_drawStringM0("SCORE"', code)

    # Fix digit positions in draw_lives() and draw_score():
    # lives digit must be at x=24; score digits must be at x=64.
    # Strategy: fix the getScreenPtr call in functions named draw_lives / draw_score.
    def _fix_digit_in_fn(src: str, fn_name: str, correct_x: int) -> str:
        # Find the function body and fix the FIRST getScreenPtr(..., <X>, 0) call inside it
        pat = re.compile(
            r'(void\s+' + re.escape(fn_name) + r'\s*\(.*?\)\s*\{[^}]*?'
            r'pv\s*=\s*cpct_getScreenPtr\s*\(\s*CPCT_VMEM_START\s*,\s*)(\d+)(\s*,\s*0\s*\))',
            re.DOTALL,
        )
        return pat.sub(lambda m: m.group(1) + str(correct_x) + m.group(3), src)

    code = _fix_digit_in_fn(code, "draw_lives", 24)
    code = _fix_digit_in_fn(code, "draw_score", 64)
    return code


def auto_fix(code: str) -> str:
    """Apply deterministic fixes to C code before writing.

    Fixes applied (in order):
    1. `define FOO bar` → `#define FOO bar`  (missing preprocessor #)
    2. Remove ball_y bottom-clamp patterns (prevent floor check from firing).
    3. Split 'TYPE *VAR = func(...)' into declaration + assignment so the
       hoisting pass can move the bare declaration to the function top.
    4. Hoist simple variable declarations above first statement in each function
       body so the code is valid C89/SDCC (prevents "syntax error: token -> 'u8'").
    """
    # Fix 1 — missing # on #define
    lines = code.splitlines()
    fixed_lines = []
    for line in lines:
        stripped = line.lstrip()
        if re.match(r"^define\s+[A-Za-z_]\w*", stripped):
            indent = line[: len(line) - len(stripped)]
            line = indent + "#" + stripped
        fixed_lines.append(line)
    code = "\n".join(fixed_lines)
    if code and not code.endswith("\n"):
        code += "\n"

    # Fix 2 — remove ball_y bottom clamp
    code = _remove_ball_y_clamp(code)

    # Fix 3 — split function-call initialisers out of declarations
    code = _split_funcall_decls(code)

    # Fix 3b — remove duplicate `u8 *pv;` declarations inside nested blocks.
    # The model sometimes declares `u8 *pv;` inside an if/for block after statements.
    # Strategy: within each function, keep only the FIRST `u8 *pv;` declaration and
    # strip any later ones (C89 doesn't allow redeclaration after statements in the
    # same or nested block).
    def _dedup_pv_decls(src: str) -> str:
        fn_pat = re.compile(
            r'(void\s+\w+\s*\([^)]*\)\s*\{)(.*?)(\n\})',
            re.DOTALL,
        )
        def _dedup(m: re.Match) -> str:
            head, body, tail = m.group(1), m.group(2), m.group(3)
            pv_re = re.compile(r'[ \t]*u8\s*\*\s*pv\s*;\s*\n')
            matches = list(pv_re.finditer(body))
            if len(matches) <= 1:
                return m.group(0)
            # Keep first, remove rest
            first_end = matches[0].end()
            new_body = body[:first_end]
            pos = first_end
            for match in matches[1:]:
                new_body += body[pos:match.start()]
                pos = match.end()
            new_body += body[pos:]
            return head + new_body + tail
        return fn_pat.sub(_dedup, src)

    code = _dedup_pv_decls(code)

    # Fix 4 — C89 declaration hoisting
    code = _hoist_c89_declarations(code)

    # Fix 3c — strip initializers from global scalar game-state variables.
    # SDCC generates __sdcc_init code for globals with initializers. This copies DATA
    # section values to RAM BEFORE main() runs, BEFORE cpct_disableFirmware() is called.
    # This can interfere with the CPC firmware state and break cpct_setPALColour/setVideoMode.
    # Master4 works because ALL game state globals have NO initializers — init_game() does it.
    # Strip initializers from globals we know init_game() will set explicitly.
    _STRIP_GLOBAL_INITS = [
        (r'\bu8\s+g_lives\s*=\s*\d+\s*;',           'u8 g_lives;'),
        (r'\bu8\s+g_score\s*=\s*\d+\s*;',           'u8 g_score;'),
        (r'\bu8\s+g_level\s*=\s*\d+\s*;',           'u8 g_level;'),
        (r'\bu8\s+game_over\s*=\s*\d+\s*;',         'u8 game_over;'),
        (r'\bu8\s+ball_launched\s*=\s*\d+\s*;',     'u8 ball_launched;'),
        (r'\bu8\s+blocks_remaining\s*=[^;]+;',       'u8 blocks_remaining;'),
        (r'\bu8\s+paddle_x\s*=\s*\d+\s*;',          'u8 paddle_x;'),
        (r'\bu8\s+prev_paddle_x\s*=\s*\d+\s*;',     'u8 prev_paddle_x;'),
        (r'\bu8\s+ball_x\s*=\s*\d+\s*,\s*ball_y\s*=\s*\d+\s*;', 'u8 ball_x, ball_y;'),
        (r'\bu8\s+ball_x\s*=\s*\d+\s*;',            'u8 ball_x;'),
        (r'\bu8\s+ball_y\s*=\s*\d+\s*;',            'u8 ball_y;'),
        (r'\bi8\s+ball_vx\s*=\s*[-\d]+\s*,\s*ball_vy\s*=\s*[-\d]+\s*;', 'i8 ball_vx, ball_vy;'),
        (r'\bi8\s+ball_vx\s*=\s*[-\d]+\s*;',        'i8 ball_vx;'),
        (r'\bi8\s+ball_vy\s*=\s*[-\d]+\s*;',        'i8 ball_vy;'),
        (r'\bu8\s+prev_ball_x\s*=\s*\d+\s*,\s*prev_ball_y\s*=\s*\d+\s*;', 'u8 prev_ball_x, prev_ball_y;'),
    ]
    # Only strip at file scope (before any function body opens)
    def _strip_global_inits(src: str) -> str:
        lines = src.splitlines()
        result = []
        in_function = False
        for line in lines:
            stripped = line.strip()
            if not in_function:
                # Detect function body start
                if re.match(r'\w.*\)\s*\{', line) and not stripped.startswith('//'):
                    in_function = True
                else:
                    for pat, replacement in _STRIP_GLOBAL_INITS:
                        if re.match(pat, stripped):
                            line = re.sub(pat, replacement, line)
                            break
            elif stripped == '}':
                in_function = False
            result.append(line)
        return '\n'.join(result)
    code = _strip_global_inits(code)

    # Fix 3d — block collision loop must exit after first hit (prevent dual-row/dual-col cancellation).
    # When ball straddles a row boundary, two rows can fire in the same frame, inverting ball_vy
    # twice (net = no change) and making ball pass through blocks. Add a hit flag to break after first.
    def _fix_block_collision_break(src: str) -> str:
        # Find the block collision for-loop and wrap it with a hit_block flag
        # Pattern: for(i...BLOCK_ROWS) { for(j...BLOCK_COLS) { if(block_grid[i][j] && AABB) { ... } } }
        # Inject: u8 hit_block = 0; ... if (!hit_block && block_grid ...) { ... hit_block = 1; }
        if 'hit_block' in src:
            return src
        # Add hit_block=0 before the outer for loop of block collision
        src = re.sub(
            r'(/\*\s*[Bb]lock\s*collision[s]?\s*\*/\s*\n\s*for\s*\(\s*i\s*=\s*0)',
            r'{\n            u8 hit_block = 0;\n            /* Block collisions */\n            for (i = 0',
            src,
        )
        # Close the outer block after the for loops
        src = re.sub(
            r'(for\s*\([^)]*BLOCK_COLS[^)]*\)\s*\{[^}]*if\s*\(\s*block_grid\[i\]\[j\])',
            r'for (j = 0; j < BLOCK_COLS; j++) {\n                if (!hit_block && block_grid[i][j]',
            src, count=1,
        )
        # Add hit_block=1 after block_grid[i][j]=0
        src = re.sub(
            r'(block_grid\[i\]\[j\]\s*=\s*0\s*;)',
            r'\1\n                    hit_block = 1;',
            src, count=1,
        )
        return src
    # NOTE: hit_block approach is complex — skip for now, rely on block_grid tracking instead
    # code = _fix_block_collision_break(code)

    # Fix 4a — block_grid state tracking MUST exist.
    # Without it, AABB fires on already-erased blocks ("ghost collision"), bouncing ball
    # at the bottom row forever and preventing it from reaching upper rows.
    # Inject block_grid[BLOCK_ROWS][BLOCK_COLS] global, init in init_game,
    # check in block collision, clear on hit, reset in reset_level.
    def _fix_block_grid(src: str) -> str:
        # Skip if already present
        if 'block_grid' in src:
            return src
        # 1. Add global declaration after block_colors
        src = re.sub(
            r'(u8\s+block_colors\s*\[\s*BLOCK_ROWS\s*\]\s*;)',
            r'\1\nu8 block_grid[BLOCK_ROWS][BLOCK_COLS];',
            src,
        )
        # 2. Initialize block_grid in init_game (after palette init, before draw blocks)
        # Find the draw block grid loop and insert grid init before it
        src = re.sub(
            r'(for\s*\([^)]*BLOCK_ROWS[^)]*\)[^{]*\{[^}]*BLOCK_COLS[^}]*cpct_drawSolidBox)',
            lambda m: (
                'for (i = 0; i < BLOCK_ROWS; i++) {\n'
                '        for (j = 0; j < BLOCK_COLS; j++) {\n'
                '            block_grid[i][j] = 1;\n'
                '        }\n'
                '    }\n    '
            ) + m.group(0),
            src, count=1,
        )
        # 3. Add block_grid check to block collision AABB
        # Find: if (ball_x... AABB condition involving BLOCK_HEIGHT or block_y
        # and add `block_grid[i][j] &&` at the start
        src = re.sub(
            r'(if\s*\()(ball_(?:x|y|right|bottom|_x|_y)\s*(?:<|>|<=|>=)[^{]+(?:BLOCK_HEIGHT|block_y|block_bottom|BLOCK_ROWS)[^{]*\{)',
            r'\1block_grid[i][j] && \2',
            src,
        )
        # 4. Add block_grid[i][j] = 0 after cpct_drawSolidBox in block collision
        src = re.sub(
            r'(cpct_drawSolidBox\s*\(\s*pv\s*,\s*0x00\s*,\s*BLOCK_WIDTH\s*,\s*BLOCK_HEIGHT\s*\)\s*;)',
            r'\1\n                    block_grid[i][j] = 0;',
            src, count=1,
        )
        # 5. Reset block_grid in reset_level
        src = re.sub(
            r'(blocks_remaining\s*=\s*BLOCK_(?:COLS|ROWS)\s*\*\s*BLOCK_(?:ROWS|COLS)\s*;)',
            r'\1\n    for (i = 0; i < BLOCK_ROWS; i++) for (j = 0; j < BLOCK_COLS; j++) block_grid[i][j] = 1;',
            src,
        )
        return src
    code = _fix_block_grid(code)

    # Fix 4b — init_game() must explicitly initialize ALL critical state variables.
    # The model often uses global initializers instead of explicit assignments in init_game().
    # In SDCC/CPCtelera the DATA section copy may not work if there are too many initialized
    # globals (e.g. u8 g_score[4]="000"), causing all globals to be 0 at runtime.
    # Inject explicit initialization after audio_init() in init_game().
    _INIT_BLOCK = (
        '\n    /* Explicit state init — always reset, never rely on global initializers */\n'
        '    g_lives = 3;\n'
        '    g_score = 0;\n'
        '    g_level = 1;\n'
        '    game_over = 0;\n'
        '    ball_launched = 0;\n'
        '    blocks_remaining = BLOCK_COLS * BLOCK_ROWS;\n'
        '    paddle_x = 35;\n'
        '    prev_paddle_x = 35;\n'
        '    ball_x = paddle_x + (PADDLE_WIDTH / 2);\n'
        '    ball_y = PADDLE_Y - BALL_H;\n'
        '    ball_vx = 1;\n'
        '    ball_vy = -1;\n'
        '    prev_ball_x = ball_x;\n'
        '    prev_ball_y = ball_y;\n'
    )
    def _fix_init_game_state(src: str) -> str:
        # Only inject if not already present (check for g_lives = 3 inside a function)
        fn_body_pat = re.compile(
            r'(void\s+init_game\s*\(\s*void\s*\)\s*\{.*?)(audio_init\s*\(\s*\)\s*;)',
            re.DOTALL,
        )
        m = fn_body_pat.search(src)
        if not m:
            return src
        # Check if g_lives = 3 is already in init_game
        if 'g_lives = 3' in m.group(0):
            return src
        # Also: g_score might be an array — if so, replace with scalar
        src = re.sub(
            r'\bu8\s+g_score\s*\[\s*\d+\s*\]\s*=[^;]+;',
            'u8 g_score;',
            src,
        )
        # Remove draw_score call that uses g_score as string (now scalar)
        # draw_score will use digit extraction so it stays
        # Inject state init
        src = fn_body_pat.sub(
            lambda mm: mm.group(1) + mm.group(2) + _INIT_BLOCK,
            src,
        )
        return src
    code = _fix_init_game_state(code)

    # Fix 5 — enforce HUD label/digit positions
    code = _fix_hud_positions(code)

    # Fix 5b — aggressive HUD fix: replace ANY getScreenPtr x-value on the line
    # immediately before drawStringM0("LIVES") or drawStringM0("LIVES:"), regardless
    # of whether it's via pv= or inline. Also fix reverse order (LIVES drawn before SCORE).
    code = re.sub(
        r'(cpct_getScreenPtr\s*\(\s*CPCT_VMEM_START\s*,\s*)\d+(\s*,\s*0\s*\)[^\n]*\n[^\n]*cpct_drawStringM0\s*\(\s*"LIVES[":][^"]*")',
        r'\g<1>0\2',
        code,
    )
    code = re.sub(
        r'(cpct_getScreenPtr\s*\(\s*CPCT_VMEM_START\s*,\s*)\d+(\s*,\s*0\s*\)[^\n]*\n[^\n]*cpct_drawStringM0\s*\(\s*"LIVES")',
        r'\g<1>0\2',
        code,
    )

    # Fix 6 — ball_vx must never be set to 0 (causes ball to go straight up/down forever)
    code = re.sub(r'\bball_vx\s*=\s*0\s*;', '', code)

    # Fix 6b — block collision must NOT have a ball_vy direction guard.
    # The model sometimes wraps the BLOCK_ROWS for-loop in `if (ball_vy > 0)` or
    # `if (ball_vy < 0)`. This skips collision when the ball moves in the opposite
    # direction: draw_game still erases the ball's previous position with 0x00, which
    # paints over live bricks, leaving a black trail through the brick area without
    # removing those bricks from block_grid ("ghost" bricks).
    # Fix: strip the if (ball_vy ...) { wrapper and its matching closing brace.
    def _remove_block_collision_vy_guard(src: str) -> str:
        lines = src.splitlines(keepends=True)
        result = []
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            if (re.match(r'if\s*\(\s*ball_vy\s*(?:[><!]=?|==)\s*', stripped)
                    and stripped.endswith('{')):
                # Peek ahead to confirm the body contains the BLOCK_ROWS for-loop
                j = i + 1
                while j < len(lines) and (not lines[j].strip() or lines[j].strip().startswith('/*')):
                    j += 1
                peek = lines[j].strip() if j < len(lines) else ''
                if 'BLOCK_ROWS' in peek or ('for' in peek and j + 1 < len(lines) and 'BLOCK' in lines[j + 1]):
                    # Emit inner body dedented by one level, skip guard and its closing brace
                    guard_indent = len(line) - len(line.lstrip())
                    inner_indent = guard_indent + 4
                    depth = 1
                    i += 1
                    while i < len(lines) and depth > 0:
                        l = lines[i]
                        s = l.strip()
                        depth += s.count('{') - s.count('}')
                        if depth > 0:
                            # Remove one indentation level if present
                            if l.startswith(' ' * inner_indent):
                                l = ' ' * guard_indent + l[inner_indent:]
                            result.append(l)
                        i += 1
                    continue
            result.append(line)
            i += 1
        return ''.join(result)
    code = _remove_block_collision_vy_guard(code)

    # Fix 6a — Space check MUST be outside the `if (!ball_launched) { } else { }` block.
    # The model often puts it inside `else { ... }` making it unreachable when ball is at rest.
    # Strategy: find the Space check inside an else block and ensure it also exists outside.
    def _fix_space_check_location(src: str) -> str:
        # Detect: Space check is inside a line where ball_launched is already 1 (else branch)
        # If the Space check `if (cpct_isKeyPressed(Key_Space) && !ball_launched)` exists
        # anywhere, we ensure a standalone version also appears BEFORE paddle movement.
        space_check_block = (
            '    if (cpct_isKeyPressed(Key_Space) && !ball_launched) {\n'
            '        ball_launched = 1;\n'
            '        ball_vx = 1;\n'
            '        ball_vy = -1;\n'
            '    }\n'
        )
        # If Space check is already at top-level scope of update_game (not inside inner braces),
        # do nothing. Otherwise inject it before paddle movement.
        if 'Key_Space' not in src:
            return src
        # Check if Space check is inside a nested block by looking for it with deep indentation
        # (4+ spaces of indent typically means nested). Top-level update_game lines have 4 spaces.
        # Inner if/else blocks have 8+ spaces.
        lines = src.splitlines()
        in_update_game = False
        brace_depth = 0
        has_toplevel_space = False
        for line in lines:
            if re.match(r'void\s+update_game\s*\(', line):
                in_update_game = True
                brace_depth = 0
                continue
            if in_update_game:
                brace_depth += line.count('{') - line.count('}')
                if brace_depth <= 0:
                    in_update_game = False
                    break
                # brace_depth==1 means we're at the top level of update_game
                if brace_depth == 1 and 'Key_Space' in line:
                    has_toplevel_space = True
                    break
        if has_toplevel_space:
            return src  # Already correctly placed
        # Inject Space check before paddle movement (Key_CursorLeft check)
        cursor_pat = re.compile(r'([ \t]*if\s*\(\s*cpct_isKeyPressed\s*\(\s*Key_CursorLeft\s*\))')
        if cursor_pat.search(src):
            src = cursor_pat.sub(space_check_block + r'\1', src, count=1)
        return src
    code = _fix_space_check_location(code)

    # Fix 6b — ball launch (Space key) must always set ball_vx=1 and ball_vy=-1.
    # Only add if a ball_vx = <value>; ASSIGNMENT is not in the next 5 lines.
    def _fix_launch_velocity(src: str) -> str:
        lines = src.splitlines()
        result = []
        i = 0
        while i < len(lines):
            result.append(lines[i])
            if re.search(r'\bball_launched\s*=\s*1\s*;', lines[i]):
                ctx = '\n'.join(lines[i+1:i+6]) if i+1 < len(lines) else ''
                # Check for ASSIGNMENT (=) not just usage
                has_vx_assign = bool(re.search(r'\bball_vx\s*=\s*[^=]', ctx))
                has_vy_assign = bool(re.search(r'\bball_vy\s*=\s*[^=]', ctx))
                indent = re.match(r'^(\s*)', lines[i]).group(1)
                if not has_vx_assign:
                    result.append(indent + 'ball_vx = 1;')
                if not has_vy_assign:
                    result.append(indent + 'ball_vy = -1;')
            i += 1
        return '\n'.join(result)
    code = _fix_launch_velocity(code)

    # Fix 6b1 — ball_x follows-paddle must use PADDLE_WIDTH/2 (gives x=40), NOT formulas giving x=39.
    # ball_x=39 means ball_right=40, straddling column boundary → dual-column block collision → ball_vy cancels.
    _BALL_X_VARIANTS = [
        r'\bball_x\s*=\s*paddle_x\s*\+\s*\(\s*PADDLE_WIDTH\s*-\s*BALL_W\s*\)\s*/\s*2\s*;',
        r'\bball_x\s*=\s*paddle_x\s*\+\s*\(\s*PADDLE_WIDTH\s*/\s*2\s*\)\s*-\s*\(\s*BALL_W\s*/\s*2\s*\)\s*;',
        r'\bball_x\s*=\s*paddle_x\s*\+\s*PADDLE_WIDTH\s*/\s*2\s*-\s*BALL_W\s*/\s*2\s*;',
        r'\bball_x\s*=\s*paddle_x\s*\+\s*\(\s*PADDLE_WIDTH\s*/\s*2\s*-\s*BALL_W\s*/\s*2\s*\)\s*;',
    ]
    for _pat in _BALL_X_VARIANTS:
        code = re.sub(_pat, 'ball_x = paddle_x + (PADDLE_WIDTH / 2);', code)

    # Fix 6b2 — (goto approach removed — too fragile with regex; rely on ball_x=40 fix instead)

    # Fix 6c — block collision must NOT have a ball_vy direction guard.
    # The model often adds `&& ball_vy > 0` or `&& ball_vy < 0` to the block
    # collision outer if(), which makes bricks unhittable in one direction.
    # Remove that guard while keeping other conditions.
    code = re.sub(
        r'(if\s*\([^)]*ball_launched[^)]*?)&&\s*ball_vy\s*[<>]=?\s*0',
        r'\1',
        code,
    )
    # Also fix the pattern: `if (ball_launched && ball_vy > 0 && ball_y >= ...)`
    code = re.sub(
        r'(if\s*\(\s*ball_launched\s*)&&\s*ball_vy\s*[<>]=?\s*0\s*&&',
        r'\1&&',
        code,
    )

    # Fix 6d — level complete inside block collision must call reset_level(),
    # NEVER set game_over = 1. Pattern: blocks_remaining == 0 → game_over = 1.
    code = re.sub(
        r'(if\s*\(\s*blocks_remaining\s*==\s*0\s*\)\s*\{[^}]*?)game_over\s*=\s*1\s*;[^}]*\}',
        r'\1g_level++; reset_level(); }',
        code, flags=re.DOTALL,
    )
    # Also fix standalone: if (blocks_remaining == 0) { game_over = 1; ... }
    code = re.sub(
        r'if\s*\(\s*blocks_remaining\s*==\s*0\s*\)\s*\{\s*game_over\s*=\s*1\s*;[^}]*\}',
        'if (blocks_remaining == 0) { g_level++; reset_level(); }',
        code, flags=re.DOTALL,
    )

    # Fix 6e — score per brick must be +=10, never ++ (g_score++ gives 1/10 the score)
    # Only fix g_score++ inside block collision context (near ball_vy inversion)
    code = re.sub(r'\bg_score\s*\+\+\s*;', 'g_score += 10;', code)

    # Fix 7 — reset_ball MUST contain: ball_launched=0, ball_x=..., ball_y=...,
    # ball_vx=1, ball_vy=-1, prev_ball_x=ball_x, prev_ball_y=ball_y.
    # Replace the entire function with the canonical version from master4.
    _RESET_BALL_PAT = re.compile(
        r'void\s+reset_ball\s*\(\s*void\s*\)\s*\{[^}]*\}',
        re.DOTALL,
    )
    if _RESET_BALL_PAT.search(code):
        # Use PADDLE_WIDTH/2 (gives 5→ball_x=40) not (PADDLE_WIDTH/2 - BALL_W/2) (gives 4→ball_x=39).
        # ball_x=39 causes dual-column block collision (straddling col4/col5 boundary at byte 40),
        # cancelling ball_vy inversions and making the ball pass through blocks.
        _CANONICAL_RESET_BALL = (
            'void reset_ball(void) {\n'
            '    ball_x = paddle_x + (PADDLE_WIDTH / 2);\n'
            '    ball_y = PADDLE_Y - BALL_H;\n'
            '    ball_vx = 1;\n'
            '    ball_vy = -1;\n'
            '    ball_launched = 0;\n'
            '    prev_ball_x = ball_x;\n'
            '    prev_ball_y = ball_y;\n'
            '}'
        )
        code = _RESET_BALL_PAT.sub(_CANONICAL_RESET_BALL, code)

    # Fix 8 — paddle collision: ball_vy must be inverted, never hardcoded to -1
    # Pattern: the paddle collision sets ball_y then ball_vy = -1 (or vice-versa).
    # Replace ball_vy = -1 that appears INSIDE the paddle collision block.
    # Detect: set ball_y = PADDLE_Y - BALL_H and immediately before/after ball_vy = -1.
    code = re.sub(
        r'(ball_y\s*=\s*PADDLE_Y\s*-\s*BALL_H\s*;[ \t]*\n[ \t]*)ball_vy\s*=\s*-1\s*;',
        r'\1ball_vy = -ball_vy;',
        code,
    )
    code = re.sub(
        r'ball_vy\s*=\s*-1\s*;([ \t]*\n[ \t]*ball_y\s*=\s*PADDLE_Y\s*-\s*BALL_H\s*;)',
        r'ball_vy = -ball_vy;\1',
        code,
    )

    # Fix 9 — "follows paddle" if(!ball_launched) block must set both ball_x AND ball_y.
    # The model often sets ball_x but forgets ball_y, leaving ball floating at y=160.
    # Find: if (!ball_launched) { ball_x = paddle_x...; } and insert ball_y if missing.
    def _fix_follows_paddle_ball_y(src: str) -> str:
        # Find the if(!ball_launched) block using a simple line-by-line scan
        lines = src.splitlines()
        result = []
        i = 0
        while i < len(lines):
            line = lines[i]
            result.append(line)
            # Detect the ball_x follows-paddle assignment
            if re.search(r'ball_x\s*=\s*paddle_x', line):
                # Check if ball_y was set within 3 lines before or after
                context = '\n'.join(lines[max(0, i-5):min(len(lines), i+5)])
                if 'ball_y' not in context and 'ball_launched' in '\n'.join(lines[max(0, i-10):i+1]):
                    # Insert ball_y = PADDLE_Y - BALL_H after this line
                    indent = re.match(r'^(\s*)', line).group(1)
                    result.append(indent + 'ball_y = PADDLE_Y - BALL_H;')
            i += 1
        return '\n'.join(result)

    code = _fix_follows_paddle_ball_y(code)

    # Fix 9c — cpct_drawCharM0 does not exist; replace with cpct_drawStringM0 + buf
    # Pattern: cpct_drawCharM0('0' + expr, pv, fg, bg)
    # Replace entire draw_lives function if it uses drawCharM0
    if 'cpct_drawCharM0' in code:
        code = re.sub(
            r'void\s+draw_lives\s*\(\s*void\s*\)\s*\{[^}]*\}',
            ('void draw_lives(void) {\n'
             '    u8 buf[2];\n'
             '    u8 *pv;\n'
             '    buf[0] = \'0\' + g_lives;\n'
             '    buf[1] = 0;\n'
             '    pv = cpct_getScreenPtr(CPCT_VMEM_START, 24, 0);\n'
             '    cpct_drawStringM0(buf, pv, 1, 0);\n'
             '}'),
            code, flags=re.DOTALL,
        )
        # Also replace any remaining cpct_drawCharM0 calls with a no-op comment
        code = re.sub(r'cpct_drawCharM0\s*\([^)]+\)\s*;', '/* cpct_drawCharM0 removed */', code)

    # Fix 9d — draw_score using g_score array directly (cpct_drawStringM0(g_score,...))
    # is wrong when g_score is now a u8 scalar. Replace with digit extraction.
    _GOOD_DRAW_SCORE = (
        'void draw_score(void) {\n'
        '    u8 buf[4];\n'
        '    u8 *pv;\n'
        '    buf[0] = \'0\' + (g_score / 100) % 10;\n'
        '    buf[1] = \'0\' + (g_score / 10) % 10;\n'
        '    buf[2] = \'0\' + g_score % 10;\n'
        '    buf[3] = 0;\n'
        '    pv = cpct_getScreenPtr(CPCT_VMEM_START, 64, 0);\n'
        '    cpct_drawStringM0(buf, pv, 1, 0);\n'
        '}'
    )
    if re.search(r'cpct_drawStringM0\s*\(\s*g_score\s*,', code):
        code = re.sub(
            r'void\s+draw_score\s*\(\s*void\s*\)\s*\{[^}]*\}',
            _GOOD_DRAW_SCORE,
            code, flags=re.DOTALL,
        )

    # Fix 10 — draw_lives: "0" + g_lives is pointer arithmetic, not char arithmetic.
    # Replace string-literal + variable with character arithmetic using a buffer.
    # Also fix draw_lives that draws a literal "0" always (ignores g_lives).
    _BAD_LIVES_PAT = re.compile(
        r'cpct_drawStringM0\s*\(\s*"0"\s*\+\s*(\w+)\s*,', re.MULTILINE
    )
    if _BAD_LIVES_PAT.search(code):
        # Replace entire draw_lives function with correct version
        _GOOD_DRAW_LIVES = (
            'void draw_lives(void) {\n'
            '    u8 buf[2];\n'
            '    u8 *pv;\n'
            '    buf[0] = \'0\' + g_lives;\n'
            '    buf[1] = 0;\n'
            '    pv = cpct_getScreenPtr(CPCT_VMEM_START, 24, 0);\n'
            '    cpct_drawStringM0(buf, pv, 1, 0);\n'
            '}'
        )
        code = re.sub(
            r'void\s+draw_lives\s*\(\s*void\s*\)\s*\{[^}]*(?:\{[^}]*\}[^}]*)?\}',
            _GOOD_DRAW_LIVES,
            code, flags=re.DOTALL,
        )

    # Fix 11 — HUD inline getScreenPtr calls (not caught by _fix_hud_positions
    # because the model calls getScreenPtr inline instead of via pv = ...).
    # Fix: cpct_drawStringM0("LIVES:", cpct_getScreenPtr(CPCT_VMEM_START, X, 0), ...)
    #   → correct X=0
    code = re.sub(
        r'(cpct_drawStringM0\s*\(\s*"LIVES:"\s*,\s*cpct_getScreenPtr\s*\(\s*CPCT_VMEM_START\s*,\s*)(\d+)(\s*,\s*0\s*\))',
        lambda m: m.group(1) + '0' + m.group(3),
        code,
    )
    code = re.sub(
        r'(cpct_drawStringM0\s*\(\s*"LIVES"\s*,\s*cpct_getScreenPtr\s*\(\s*CPCT_VMEM_START\s*,\s*)(\d+)(\s*,\s*0\s*\))',
        lambda m: m.group(1) + '0' + m.group(3),
        code,
    )
    code = re.sub(
        r'(cpct_drawStringM0\s*\(\s*"SCORE"\s*,\s*cpct_getScreenPtr\s*\(\s*CPCT_VMEM_START\s*,\s*)(\d+)(\s*,\s*0\s*\))',
        lambda m: m.group(1) + '40' + m.group(3),
        code,
    )
    return code


def check(code: str) -> GuardResult:
    """Scan C code for forbidden/unknown API calls and missing boilerplate."""
    errors:   list[str] = []
    warnings: list[str] = []

    # 1. Bare `define` without `#` → hard error (auto_fix handles it if called first)
    bare = re.findall(r"(?m)^[ \t]*define\s+[A-Za-z_]\w*", code)
    if bare:
        errors.append(
            f"MISSING #: {len(bare)} directive(s) written as 'define' instead of '#define' "
            f"— e.g. {bare[0]!r} (use auto_fix() to repair automatically)"
        )

    # 2. C89 declaration-after-statement (simplified heuristic per function block)
    _TYPES = r"(?:u8|i8|u16|i16|u32|i32|void\s*\*|char|int|unsigned|signed)"
    _TYPE_DECL = re.compile(rf"^\s*{_TYPES}\s+\w+")
    _STATEMENT  = re.compile(r"^\s*\w+\s*(?:[=\[(]|[-+][-+])")  # assignment, call, increment
    in_block: list[bool] = [False]  # stack: True = block already had a statement
    depth = 0
    for line in code.splitlines():
        s = line.strip()
        if not s or s.startswith("//") or s.startswith("/*") or s.startswith("*"):
            continue
        # Preprocessor directives are not C statements.
        if s.startswith("#"):
            # #else / #elif starts a new conditional branch — reset the "seen a statement"
            # flag so declarations in the else-branch are not wrongly flagged as post-statement.
            if s.startswith("#else") or s.startswith("#elif"):
                if in_block:
                    in_block[-1] = False
            continue
        opens  = s.count("{")
        closes = s.count("}")
        if opens > closes:          # entering block
            in_block.extend([False] * (opens - closes))
            depth += opens - closes
        elif closes > opens:        # leaving block(s)
            pop = min(closes - opens, len(in_block) - 1)
            in_block = in_block[: max(1, len(in_block) - pop)]
            depth = max(0, depth - (closes - opens))
        if in_block and in_block[-1] and _TYPE_DECL.match(line):
            errors.append(
                f"C89 VIOLATION: variable declared after statement in same block — "
                f"'{s[:60]}'. Move ALL declarations to the top of the enclosing block."
            )
            break   # one error is enough to flag the issue
        if in_block and _STATEMENT.match(line):
            in_block[-1] = True

    # 3. Forbidden calls → hard errors
    for fn in sorted(_FORBIDDEN):
        if re.search(rf"\b{re.escape(fn)}\s*\(", code):
            errors.append(
                f"FORBIDDEN: {fn}() does not exist in CPCtelera/SDCC — "
                "use the digit-display pattern instead"
            )

    # 3. Unknown cpct_* calls → warnings
    all_cpct = set(re.findall(r"\bcpct_\w+\b", code))
    unknown  = all_cpct - _KNOWN_CPCT - _FORBIDDEN
    for fn in sorted(unknown):
        warnings.append(f"UNVERIFIED cpct call: {fn} — not in known API; verify before compiling")

    # 4. Full-screen clear inside a game loop → BLACK SCREEN
    #    Catches BOTH:
    #      a) cpct_memset(CPCT_VMEM_START, ...) — fills all 16KB
    #      b) cpct_drawSolidBox(ptr, X, 80, 200)  — width=80 height=200 = full Mode0 screen
    #    Strategy: flag any of these patterns that appear AFTER the first while() line
    #    and are indented ≥ 4 spaces (i.e. inside the loop body or a called draw function).
    _FULLCLEAR_RE = re.compile(
        r"\bcpct_memset\s*\(\s*CPCT_VMEM_START\b"
        r"|\bcpct_drawSolidBox\s*\([^,]+,\s*(?:0x00|0)\s*,\s*80\s*,\s*200\s*\)"
    )
    if _FULLCLEAR_RE.search(code):
        _lines_fc = code.splitlines()
        _after_while = False
        for _ln in _lines_fc:
            if re.search(r"\bwhile\s*\(", _ln):
                _after_while = True
            if _after_while and _FULLCLEAR_RE.search(_ln):
                if len(_ln) - len(_ln.lstrip()) >= 4:
                    errors.append(
                        "BLACK SCREEN: full-screen clear is inside the game loop "
                        "(cpct_memset(CPCT_VMEM_START,...) or cpct_drawSolidBox(...,0x00,80,200)). "
                        "Clearing 16KB at 4MHz Z80 costs 12-18ms = 60-90% of a 20ms frame; "
                        "the screen appears completely BLACK. "
                        "FIX: call cpct_memset ONCE at init (before while(1)), then use the "
                        "erase/draw pattern per entity every frame: "
                        "cpct_drawSolidBox(pvmem_old, 0x00, W, H) → update pos → "
                        "cpct_drawSolidBox(pvmem_new, COLOR, W, H)."
                    )
                    break

    # 5. cpct_isKeyPressed used but cpct_scanKeyboard/_f absent → keyboard always silent
    if re.search(r"\bcpct_isKeyPressed\s*\(", code):
        if not re.search(r"\bcpct_scanKeyboard(?:_f)?\s*\(", code):
            errors.append(
                "MISSING cpct_scanKeyboard: cpct_isKeyPressed() is used but neither "
                "cpct_scanKeyboard() nor cpct_scanKeyboard_f() is ever called. "
                "Without it, all key checks return false — keyboard is completely "
                "silent. Add: cpct_scanKeyboard_f(); in the main while(1) loop, once per frame, "
                "BEFORE any cpct_isKeyPressed() call."
            )
        else:
            # scanKeyboard/_f is present — check it is in the main while loop, not buried in a subfunction
            scan_lines = [ln for ln in code.splitlines() if re.search(r"\bcpct_scanKeyboard(?:_f)?\s*\(", ln)]
            all_deep = all(len(ln) - len(ln.lstrip()) > 8 for ln in scan_lines)
            if all_deep:
                warnings.append(
                    "cpct_scanKeyboard() appears to be inside a nested function, not in the main "
                    "while(1) loop. It must be called once per frame at the top level of the game "
                    "loop to update the keyboard state before cpct_isKeyPressed() calls."
                )

    # 6. cpct_setPalette without cpct_fw2hw → all colours black/wrong (RULE-012)
    if re.search(r"\bcpct_setPalette\s*\(", code):
        if not re.search(r"\bcpct_fw2hw\s*\(", code):
            errors.append(
                "MISSING cpct_fw2hw: cpct_setPalette() is present but cpct_fw2hw() is not. "
                "FW_* colour constants must be converted to hardware values before calling "
                "cpct_setPalette — otherwise all pens map to wrong colours and the screen "
                "appears black or garbage. Add: cpct_fw2hw(g_pal, N); before cpct_setPalette(g_pal, N);"
            )

    # 6. i8 variables compared to values > 127 → always false / wrong (i8 max = 127)
    #    Heuristic: find i8 var declarations, then check if they appear in comparisons
    #    with literals > 127.
    i8_vars = set(re.findall(r"\bi8\s+(\w+)", code))
    if i8_vars:
        for var in i8_vars:
            for m in re.finditer(
                rf"\b{re.escape(var)}\b\s*(?:>=|<=|>|<|==)\s*(\d+)", code
            ):
                val = int(m.group(1))
                if val > 127:
                    errors.append(
                        f"TYPE ERROR: i8 variable '{var}' compared to value(s) [{val}] which exceed "
                        f"i8 max (127). This produces wrong/undefined behaviour. "
                        f"Use u8 for coordinates (ball_y, paddle_y) which are always positive."
                    )
                    break

    # 7. Palette declared with pixel-byte literals instead of FW_* constants.
    #    cpct_fw2hw expects FW_* indices (0..26). Pixel bytes like 0x03/0x0C/0x0F
    #    get reinterpreted as wrong colours → screen looks black or single-colour.
    pal_m = re.search(
        r"\bu8\s+\w*pal\w*\s*\[\s*\]?\s*\]?\s*=\s*\{([^}]+)\}", code, re.IGNORECASE
    )
    if pal_m and re.search(r"\bcpct_fw2hw\s*\(", code):
        items = [s.strip() for s in pal_m.group(1).split(",")]
        # If none of the entries use an FW_ constant, very likely raw pen bytes
        if items and not any("FW_" in it for it in items):
            errors.append(
                "PALETTE ERROR: palette array uses raw pixel bytes (e.g. 0x00, 0x03, 0x0C, 0x0F) "
                "instead of FW_* constants. cpct_fw2hw() expects firmware indices (FW_BLACK, "
                "FW_BRIGHT_WHITE, FW_BRIGHT_RED, FW_BRIGHT_YELLOW, etc.). Passing pixel bytes "
                "produces wrong colours — the screen appears mostly black or single-coloured. "
                "Use: u8 g_pal[4] = {FW_BLACK, FW_BRIGHT_WHITE, FW_BRIGHT_RED, FW_BRIGHT_YELLOW};"
            )

    # 8. (removed — cpct_waitVSYNC position is project-style, both at start and end work)

    # 8b. Wrong pen bytes in draw calls — Mode 0 pixel encoding (hardware-verified):
    #   pen N byte = N uses bits 7,5,3,1 for left pixel and 6,4,2,0 for right pixel:
    #   pen0=0x00  pen1=0x03  pen2=0x0C  pen3=0x0F   ← ONLY valid with 4-entry palette
    #   pen4=0x30  pen5=0x33  pen6=0x3C  pen7=0x3F
    #   pen8=0xC0  pen9=0xC3  pen10=0xCC pen11=0xCF   ← outside 4-entry palette!
    #   NOTE: 0xC0 = pen8, 0xCC = pen10 — NOT pen1/pen3. Using them gives wrong colours.
    _MODE0_BYTE_TO_PEN: dict[int, int] = {
        0x00: 0,  0x03: 1,  0x0C: 2,  0x0F: 3,
        0x30: 4,  0x33: 5,  0x3C: 6,  0x3F: 7,
        0xC0: 8,  0xC3: 9,  0xCC: 10, 0xCF: 11,
        0xF0: 12, 0xF3: 13, 0xFC: 14, 0xFF: 15,
    }
    pal_n_m = re.search(r"\bcpct_setPalette\s*\([^,]+,\s*(\d+)\s*\)", code)
    if pal_n_m:
        pal_n = int(pal_n_m.group(1))
        # Bytes whose pen index >= pal_n → outside palette → wrong colour
        out_of_palette = {b: p for b, p in _MODE0_BYTE_TO_PEN.items() if p >= pal_n}
        usages: list[tuple[int, str]] = []
        for m in re.finditer(
            r"\bcpct_drawSolidBox\s*\(\s*[^,]+,\s*(0x[0-9A-Fa-f]{2}|\d+)", code,
        ):
            try:
                val = int(m.group(1), 0)
                if val in out_of_palette:
                    usages.append((val, "cpct_drawSolidBox"))
            except ValueError:
                pass
        for m in re.finditer(
            r"\bcpct_drawStringM0\s*\([^,]+,\s*[^,]+,\s*(0x[0-9A-Fa-f]{2}|\d+)\s*,\s*(0x[0-9A-Fa-f]{2}|\d+)",
            code,
        ):
            for grp in (m.group(1), m.group(2)):
                try:
                    val = int(grp, 0)
                    if val in out_of_palette and val != 0x00:
                        usages.append((val, "cpct_drawStringM0"))
                except ValueError:
                    pass
        if usages:
            seen: set = set()
            uniq: list = []
            for v, where in usages:
                if (v, where) not in seen:
                    seen.add((v, where)); uniq.append((v, where))
            msg_parts = [f"0x{v:02X}=pen{out_of_palette[v]} in {w}" for v, w in uniq[:5]]
            errors.append(
                f"WRONG PEN BYTE(S): {', '.join(msg_parts)}. "
                f"With cpct_setPalette(g_pal, {pal_n}) only pens 0..{pal_n-1} are defined. "
                "Mode 0 correct bytes: pen0=0x00  pen1=0x03  pen2=0x0C  pen3=0x0F. "
                "Common mistake: 0xC0 is pen8 and 0xCC is pen10 — NOT pen1/pen3. "
                "Replace with the correct bytes from the table above."
            )

    # 9. Velocity variable declared but increment uses literal ++ / -- instead of += vx.
    #    Heuristic: an i8 velocity var initialised to a value with magnitude >= 2 that is
    #    never used in a `pos += var` or `pos -= var` pattern → the velocity is ignored.
    for vm in re.finditer(r"\bi8\s+(\w*_?v[xy]\w*)\s*=\s*(-?\d+)", code):
        vname, vval = vm.group(1), int(vm.group(2))
        if abs(vval) >= 2:
            # Look for `something += vname` or `something -= vname`
            used = re.search(rf"[+\-]=\s*{re.escape(vname)}\b|=\s*\w+\s*[+\-]\s*{re.escape(vname)}\b", code)
            if not used:
                warnings.append(
                    f"VELOCITY IGNORED: '{vname}' is initialised to {vval} (magnitude >= 2) but is "
                    f"never used in 'pos += {vname}' / 'pos -= {vname}'. The code increments by 1 per "
                    f"frame regardless of the velocity value, so the entity moves much slower than "
                    f"intended. Use: if ({vname} > 0) pos += {vname}; else pos += {vname}; (or pos += {vname} unconditionally with bounds checks)."
                )

    # 10. u8 variable compared `< 0` → always false (warning from SDCC, logic bug).
    u8_vars = set(re.findall(r"\bu8\s+(\w+)", code))
    for var in u8_vars:
        if re.search(rf"\b{re.escape(var)}\s*<\s*0\b", code):
            errors.append(
                f"TYPE ERROR: u8 variable '{var}' compared `< 0` — always false (unsigned). "
                f"After 'paddle_x -= 3' with paddle_x=1 the value underflows to 254. "
                f"Use a signed temporary or check BEFORE subtracting: "
                f"if ({var} >= STEP) {var} -= STEP; else {var} = 0;"
            )

    # 12. char buffer declared but NEVER written before being passed to cpct_drawStringM0
    #     → prints uninitialised stack garbage. Very common when the model "remembers"
    #     it should display a number but forgets the digit-to-string conversion.
    for cm in re.finditer(r"\bchar\s+(\w+)\s*\[\s*\d+\s*\]\s*;", code):
        bname = cm.group(1)
        # Look for any write into the buffer: bname[i] = ..., bname[0] = ..., or
        # a call that takes &bname / bname as out-param (memset/memcpy/strcpy/etc are forbidden,
        # so the only legitimate way is element-wise assignment or a manual digit-pack loop).
        written = re.search(
            rf"\b{re.escape(bname)}\s*\[\s*\w+\s*\]\s*=",
            code,
        )
        used_in_draw = re.search(
            rf"\bcpct_drawString(?:M0|M1|M2)\s*\(\s*{re.escape(bname)}\b",
            code,
        )
        if used_in_draw and not written:
            errors.append(
                f"UNINITIALISED STRING BUFFER: 'char {bname}[N]' is declared and passed to "
                f"cpct_drawStringM0(...) but is NEVER written to (no '{bname}[i] = ...' anywhere). "
                f"The function will print random stack garbage in HUD area. "
                f"FIX: convert the integer manually before drawing. Pattern: "
                f"{bname}[0] = '0' + (value / 100) % 10; {bname}[1] = '0' + (value / 10) % 10; "
                f"{bname}[2] = '0' + value % 10; {bname}[3] = 0; "
                f"(sprintf/itoa do not exist — they are in _FORBIDDEN)."
            )

    # 13. Multiple cpct_drawStringM0 calls at the SAME y coordinate with overlapping x ranges.
    #     In Mode 0 each character is 4 bytes wide (8 pixels = 4 bytes at 2 pixels/byte).
    #     Overlap → strings render on top of each other. Heuristic: collect (y, x, byte_len)
    #     triples from getScreenPtr+drawStringM0 pairs and warn if two share y and overlap.
    hud_strings: list[tuple[int, int, int, str]] = []  # (y, x, byte_len, text)
    # Match a pair of consecutive statements: pv = cpct_getScreenPtr(START, X, Y); cpct_drawStringM0("TEXT", pv, ...);
    pair_re = re.compile(
        r"cpct_getScreenPtr\s*\(\s*CPCT_VMEM_START\s*,\s*(\d+)\s*,\s*(\d+)\s*\)\s*;\s*"
        r"cpct_drawStringM0\s*\(\s*\"([^\"]*)\"",
        re.DOTALL,
    )
    for m in pair_re.finditer(code):
        x = int(m.group(1)); y = int(m.group(2)); text = m.group(3)
        hud_strings.append((y, x, 4 * len(text), text))
    for i in range(len(hud_strings)):
        y1, x1, l1, t1 = hud_strings[i]
        for j in range(i + 1, len(hud_strings)):
            y2, x2, l2, t2 = hud_strings[j]
            # Same x → almost certainly a redraw/update of the same HUD field (not an overlap bug)
            if y1 == y2 and x1 != x2 and x1 < x2 + l2 and x2 < x1 + l1:
                warnings.append(
                    f"OVERLAPPING HUD STRINGS at y={y1}: '{t1}' at x={x1} (width {l1} bytes) "
                    f"overlaps '{t2}' at x={x2} (width {l2} bytes). Each Mode 0 character is 2 bytes wide. "
                    f"Separate them: place '{t2}' at x>={x1 + l1} or use different y."
                )
                break

    # 14. Missing required boilerplate
    if "#include <cpctelera.h>" not in code:
        errors.append("MISSING: #include <cpctelera.h>")

    if not re.search(r"\bvoid\s+main\s*\(\s*void\s*\)", code):
        errors.append("MISSING: void main(void) — SDCC requires this exact signature")

    # -------------------------------------------------------------------------
    # Generic platform checks — apply to any CPCtelera game
    # -------------------------------------------------------------------------

    # 15. cpct_drawSolidBox x+width overflow (> 80 bytes screen width)
    #     Pattern: cpct_getScreenPtr(VMEM_START, X, Y) then IMMEDIATELY cpct_drawSolidBox(ptr, c, W, H).
    #     "Immediately" = no intervening `;` (i.e. no other statement reassigns pv between them).
    #     Using DOTALL with .*? was pairing calls across function boundaries (false positives).
    _sbox_re = re.compile(
        r"cpct_getScreenPtr\s*\(\s*CPCT_VMEM_START\s*,\s*(\d+)\s*,\s*(\d+)\s*\)"
        r"[^;]*;\s*"
        r"cpct_drawSolidBox\s*\(\s*\w+\s*,\s*[^,]+,\s*(\d+)\s*,\s*(\d+)",
    )
    for m in _sbox_re.finditer(code):
        x, y, w, h = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
        if x + w > 80:
            errors.append(
                f"SCREEN OVERFLOW (X): cpct_drawSolidBox at x={x} width={w} → "
                f"rightmost byte={x+w-1} exceeds screen width (79). "
                f"Mode 0 screen is 80 bytes wide (0..79). Reduce width or move left: "
                f"width must be ≤ {80 - x}."
            )
        if y + h > 200:
            errors.append(
                f"SCREEN OVERFLOW (Y): cpct_drawSolidBox at y={y} height={h} → "
                f"bottom pixel={y+h-1} exceeds screen height (199). "
                f"Mode 0 screen is 200 pixels tall (0..199). Reduce height or move up."
            )

    # 16. cpct_getScreenPtr with out-of-range constant arguments
    for m in re.finditer(
        r"cpct_getScreenPtr\s*\(\s*CPCT_VMEM_START\s*,\s*(\d+)\s*,\s*(\d+)", code
    ):
        x, y = int(m.group(1)), int(m.group(2))
        if x >= 80:
            errors.append(
                f"OUT OF RANGE: cpct_getScreenPtr x={x} ≥ 80. "
                f"Mode 0 x must be 0..79 (bytes). This computes an address outside "
                f"the screen buffer → memory corruption."
            )
        if y >= 200:
            errors.append(
                f"OUT OF RANGE: cpct_getScreenPtr y={y} ≥ 200. "
                f"Mode 0 y must be 0..199 (pixels). This computes an address outside "
                f"the screen buffer → memory corruption."
            )

    # 17. cpct_drawStringM0 x + len*4 overflow (string literal version)
    #     4 bytes per character in Mode 0 (8 pixels wide, 2 px/byte).
    #     Only pair getScreenPtr + drawStringM0 that are CONSECUTIVE (no intervening `;`).
    _str_re = re.compile(
        r"cpct_getScreenPtr\s*\(\s*CPCT_VMEM_START\s*,\s*(\d+)\s*,\s*\d+\s*\)"
        r"[^;]*;\s*"
        r'cpct_drawStringM0\s*\(\s*"([^"]*)"',
    )
    for m in _str_re.finditer(code):
        x, text = int(m.group(1)), m.group(2)
        byte_width = len(text) * 4
        if x + byte_width > 80:
            errors.append(
                f"STRING OVERFLOW: \"{text}\" ({len(text)} chars × 4 bytes = {byte_width} bytes) "
                f"starting at x={x} → writes bytes {x}..{x+byte_width-1}, "
                f"but screen ends at byte 79. "
                f"Max chars from x={x}: {(80-x)//4}. Shorten the string or start at x=0."
            )

    # 18. u8 variable compared with <= 0 (always false — unsigned can never be negative)
    #     Complements check 10 which only catches < 0
    u8_vars_all = set(re.findall(r"\bu8\s+(\w+)", code))
    for var in u8_vars_all:
        if re.search(rf"\b{re.escape(var)}\s*<=\s*0\b", code):
            warnings.append(
                f"UNSIGNED COMPARISON: u8 '{var}' compared '<= 0' — this means only '== 0' "
                f"is ever true (u8 wraps to 255 on decrement from 0, never goes negative). "
                f"Use '== 0' instead of '<= 0', or declare as i8 if negative values are intended."
            )

    # 19. cpct_waitVSYNC absent in a file with while(1) — game runs at full CPU speed
    if re.search(r"\bwhile\s*\(\s*1\s*\)", code):
        if not re.search(r"\bcpct_waitVSYNC\s*\(", code):
            errors.append(
                "MISSING cpct_waitVSYNC: the file has a while(1) loop but never calls "
                "cpct_waitVSYNC(). Without it the game runs at full Z80 speed (4 MHz), "
                "not at 50 fps. Add: cpct_waitVSYNC(); at the end of the main loop."
            )

    # 20. Grid dimension overflow: COLS*BLOCK_W > 80 or ROWS*BLOCK_H + start_y > 200
    #     Detects when a tile grid would exceed screen boundaries.
    _defines: dict[str, int] = {}
    for m in re.finditer(r"#define\s+(\w+)\s+(\d+)", code):
        try:
            _defines[m.group(1)] = int(m.group(2))
        except ValueError:
            pass

    def _resolve(name: str) -> int | None:
        """Return integer value of a name that is either a literal or a #define."""
        try:
            return int(name)
        except ValueError:
            return _defines.get(name)

    # Find COLS/ROWS and BLOCK_W/BLOCK_H candidates (any #define whose name
    # contains COL/ROW and WIDTH/HEIGHT case-insensitively)
    cols_names  = [k for k in _defines if re.search(r"col", k, re.I)]
    rows_names  = [k for k in _defines if re.search(r"row", k, re.I)]
    # Use word-boundary anchors so BLOCK_ROWS (contains 'W' in 'ROW') does not
    # match as a block-width candidate.
    bw_names    = [k for k in _defines if re.search(r"(block_?width|bw$|b_w$|tile_?width)", k, re.I)]
    bh_names    = [k for k in _defines if re.search(r"(block_?height|bh$|b_h$|tile_?height)", k, re.I)]

    for cn in cols_names:
        for bwn in bw_names:
            cols, bw = _defines[cn], _defines[bwn]
            if cols * bw > 80:
                errors.append(
                    f"GRID OVERFLOW (X): {cn}={cols} × {bwn}={bw} = {cols*bw} bytes "
                    f"> 80 (screen width). The tile grid overflows the right edge. "
                    f"Reduce columns or block width so COLS × BLOCK_W ≤ 80."
                )
            elif cols * bw < 80:
                warnings.append(
                    f"GRID GAP (X): {cn}={cols} × {bwn}={bw} = {cols*bw} bytes "
                    f"< 80 (screen width). The tile grid leaves {80 - cols*bw} bytes "
                    f"of unused space on the right. Consider adjusting to fill the screen."
                )

    for rn in rows_names:
        for bhn in bh_names:
            rows, bh = _defines[rn], _defines[bhn]
            if rows * bh > 200:
                errors.append(
                    f"GRID OVERFLOW (Y): {rn}={rows} × {bhn}={bh} = {rows*bh} pixels "
                    f"> 200 (screen height). The tile grid overflows the bottom edge."
                )

    return GuardResult(ok=len(errors) == 0, errors=errors, warnings=warnings)


def print_report(result: GuardResult) -> None:
    """Pretty-print the guard result to stdout."""
    if result.ok and not result.warnings:
        print(f"{_G}  ✓ CODE GUARD — no forbidden calls detected{_RS}")
        return
    if result.errors:
        print(f"\n{_R}{_B}  ✗ CODE GUARD — {len(result.errors)} forbidden call(s):{_RS}")
        for e in result.errors:
            print(f"  {_R}  • {e}{_RS}")
    if result.warnings:
        print(f"\n{_Y}  ⚠ CODE GUARD — {len(result.warnings)} unverified call(s):{_RS}")
        for w in result.warnings:
            print(f"  {_Y}  • {w}{_RS}")
