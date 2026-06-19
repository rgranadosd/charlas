# C89/SDCC Code Generation Rules for CPCtelera

These rules apply to ALL C code generated for Amstrad CPC with CPCtelera + SDCC compiler.
Violations cause build failures. These are real errors seen in generated code.

---

## MUST-HAVE CHECKLIST — Every generated main.c must pass these three tests

Before considering any file complete, verify:

| # | Check | Symptom if missing |
|---|-------|--------------------|
| 1 | `cpct_scanKeyboard_f()` is in `while(1)` loop, once per frame | Keyboard completely silent — no input ever registers |
| 2 | `cpct_setPALColour(pen, HW_COLOR)` called for each pen in `init_game` | Screen black or random garbage colours |
| 3 | Screen positions use `u8`, velocities use `i8` | SDCC warning 94/158, ball stuck at y<127, floor never reached |

---

## RULE-001: Variable Declarations MUST Come Before Any Statement (C89)

**Compiler error:** `syntax error: token -> 'u8' ; column N`
**Also:** `error 20: Undefined identifier 'i'` (for variables declared after statements)

**Why it fails:** SDCC compiles in C89 mode. In C89, all variable declarations in a block
MUST appear before any executable statement. C99/C++ style "declare when first used" is NOT valid.

**WRONG — Causes "syntax error: token -> 'u8'":**
```c
void init_game(void) {
    g_score = 0;      /* statement */
    g_lives = 3;      /* statement */
    /* Initialise loop */
    u8 i, j;          /* ERROR: declaration after statement */
    for (i = 0; i < ROWS; i++) { ... }
}
```

**WRONG — Same error in update function:**
```c
void update_game(void) {
    ball_x += ball_vx;   /* statement */
    ball_y += ball_vy;   /* statement */
    /* Block collisions */
    u8 i, j;             /* ERROR: declaration after statement */
    for (i = 0; i < ROWS; i++) { ... }
}
```

**CORRECT — All declarations at the TOP of the block:**
```c
void init_game(void) {
    u8 i, j;          /* ALL declarations FIRST */
    g_score = 0;      /* then statements */
    g_lives = 3;
    for (i = 0; i < ROWS; i++) {
        for (j = 0; j < COLS; j++) {
            blocks[i][j] = 1;
        }
    }
}

void update_game(void) {
    u8 i, j;             /* ALL declarations FIRST */
    ball_x += ball_vx;
    ball_y += ball_vy;
    for (i = 0; i < ROWS; i++) {
        for (j = 0; j < COLS; j++) {
            if (blocks[i][j]) { ... }
        }
    }
}
```

**Key principle:** The "Initialise loop variables" comment does NOT excuse placing `u8 i, j`
after statements. Move the declarations to the very first lines of the function body.

---

## RULE-002: Declarations With Function-Call Initialisers Must Also Be First

**WRONG:**
```c
void f(void) {
    cpct_disableFirmware();        /* statement */
    u8* pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, 0);  /* ERROR */
}
```

**CORRECT:**
```c
void f(void) {
    u8* pvmem;                     /* declaration first */
    cpct_disableFirmware();
    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, 0);  /* assignment later */
}
```

---

## RULE-003: Unsigned Types Cannot Be Less Than Zero

**Compiler warning:** `warning 94: comparison is always false due to limited range of data type`

`u8` is unsigned (0–255). After `g_lives--` when g_lives is 0, it wraps to 255.

**WRONG:**
```c
u8 g_lives = 3;
g_lives--;
if (g_lives <= 0) {  /* WARNING: u8 can never be < 0, always false except at 0 */
```

**CORRECT:**
```c
u8 g_lives = 3;
g_lives--;
if (g_lives == 0) {  /* correct */
```

Or use `i8` (signed, -128 to 127) for values that may go negative:
```c
i8 g_lives = 3;
g_lives--;
if (g_lives <= 0) {  /* OK: i8 can be negative */
```

---

## RULE-004: No Standard Library Functions

SDCC for Z80/CPC does not link stdlib. These cause link errors:

| Forbidden | Replacement |
|-----------|-------------|
| `abs(x)` | `((x)<0?-(x):(x))` |
| `printf(...)` | `cpct_drawStringM0(...)` |
| `sprintf(...)` | manual digit extraction |
| `strlen`, `strcpy`, etc. | manual loops |
| `malloc`, `free` | static arrays only |

---

## RULE-005: Correct Function Signatures

```c
void main(void)                        /* NOT int main() */
void draw_score(void)                  /* NOT void draw_score() */
```

SDCC expects `void main(void)` as the entry point for CPC programs.

---

## RULE-006: Template for a Correct CPCtelera Function With Loops

```c
/* CORRECT template — all declarations at top, then statements */
void draw_blocks(void) {
    u8 i, j;                                     /* loop variables: FIRST */
    u8* pvmem;                                   /* pointer: FIRST */

    for (i = 0; i < ROWS; i++) {
        for (j = 0; j < COLS; j++) {
            if (blocks[i][j]) {
                pvmem = cpct_getScreenPtr(CPCT_VMEM_START, j * 4, i * 8 + 20);
                cpct_drawSolidBox(pvmem, 0x0C, 4, 8);
            }
        }
    }
}
```

---

## RULE-007: Complete Correct main.c Skeleton

**Invariants ALL generated code must satisfy:**
1. Palette via `cpct_setPALColour(pen, HW_COLOR)` per pen — NEVER `cpct_fw2hw`/`cpct_setPalette`.
2. Screen clear via `cpct_clearScreen(0)` ONLY in `init_game()` — NEVER inside `while(1)`.
3. Colours via `cpct_px2byteM0(pen, pen)` — NEVER hardcoded bytes like `0x03`, `0x0F`.
4. Keyboard via `cpct_scanKeyboard_f()` — NEVER `cpct_scanKeyboard()`.
5. Screen pointer `u8 *pv` declared ONCE at top of function, assigned (no type) throughout.

**Position variables are `u8`. Velocity/delta variables are `i8`. See RULE-009.**

```c
#include <cpctelera.h>

#define BLOCK_WIDTH  8
#define BLOCK_HEIGHT 8
#define BLOCK_ROWS   5
#define BLOCK_COLS   10
#define BALL_W       2
#define BALL_H       4
#define PADDLE_Y     190
#define PADDLE_WIDTH 10
#define FLOOR_Y      195

u8 g_score = 0;
u8 g_lives  = 3;
u8 ball_x,  ball_y;
i8 ball_vx, ball_vy;
u8 paddle_x;
u8 prev_ball_x, prev_ball_y, prev_paddle_x;
u8 g_ball_color, g_paddle_color;
u8 block_colors[BLOCK_ROWS];
u8 block_grid[BLOCK_ROWS][BLOCK_COLS];

void init_game(void) {
    u8 i, j;
    u8 *pv;                        /* declared ONCE at top */

    /* Runtime state — always initialise explicitly here */
    g_score = 0; g_lives = 3;
    paddle_x = 35;
    ball_x = paddle_x + (PADDLE_WIDTH >> 1);
    ball_y = PADDLE_Y - BALL_H - 1;
    ball_vx = 1; ball_vy = -1;
    prev_ball_x = ball_x; prev_ball_y = ball_y;
    prev_paddle_x = paddle_x;

    /* Hardware init — use cpct_setPALColour, NOT cpct_fw2hw/cpct_setPalette */
    cpct_disableFirmware();
    cpct_setVideoMode(0);
    cpct_setPALColour(0, HW_BLACK);
    cpct_setPALColour(1, HW_BRIGHT_WHITE);
    cpct_setPALColour(2, HW_BRIGHT_RED);
    cpct_setPALColour(3, HW_BRIGHT_GREEN);
    cpct_setBorder(HW_BLACK);

    /* Screen clear — ONCE here only, NEVER inside while(1) */
    cpct_clearScreen(0);

    /* Colour bytes — use cpct_px2byteM0, NOT hardcoded bytes */
    g_ball_color   = cpct_px2byteM0(1, 1);
    g_paddle_color = cpct_px2byteM0(2, 2);
    block_colors[0] = cpct_px2byteM0(2, 2);
    block_colors[1] = cpct_px2byteM0(3, 3);
    block_colors[2] = cpct_px2byteM0(1, 1);
    block_colors[3] = cpct_px2byteM0(3, 3);
    block_colors[4] = cpct_px2byteM0(2, 2);

    /* Init and draw block grid */
    for (i = 0; i < BLOCK_ROWS; i++) {
        for (j = 0; j < BLOCK_COLS; j++) {
            block_grid[i][j] = 1;
            pv = cpct_getScreenPtr(CPCT_VMEM_START, j * BLOCK_WIDTH, 20 + i * BLOCK_HEIGHT);
            cpct_drawSolidBox(pv, block_colors[i], BLOCK_WIDTH, BLOCK_HEIGHT);
        }
    }

    /* Draw HUD labels once */
    pv = cpct_getScreenPtr(CPCT_VMEM_START, 0, 0);
    cpct_drawStringM0("LIVES", pv, cpct_px2byteM0(1,1), 0x00);
    pv = cpct_getScreenPtr(CPCT_VMEM_START, 48, 0);
    cpct_drawStringM0("SCORE", pv, cpct_px2byteM0(1,1), 0x00);
}

void update_game(void) {
    u8 i, j, *pv;
    u8 ball_right;

    /* Step 1: Ball follows paddle OR moves (if launched).
       Floor check is INSIDE the Y movement — NOT a separate if at the end. */
    if (!ball_launched) {
        /* Ball rests on paddle — update position every frame */
        ball_x = paddle_x + (PADDLE_WIDTH / 2) - (BALL_W / 2);
        ball_y = PADDLE_Y - BALL_H;
    } else {
        /* Horizontal movement — lookahead before moving */
        if (ball_vx > 0) {
            if (ball_x + BALL_W - 1 < 79) ball_x++;
            else { ball_vx = -1; audio_play_sfx(SFX_WALL_HIT); }
        } else {
            if (ball_x > 0) ball_x--;
            else { ball_vx = 1; audio_play_sfx(SFX_WALL_HIT); }
        }

        /* Vertical movement — floor check is the ELSE of the move, not separate */
        if (ball_vy < 0) {
            if (ball_y > 0) ball_y--;
            else { ball_vy = 1; audio_play_sfx(SFX_WALL_HIT); }
        } else {
            ball_bottom = ball_y + BALL_H - 1;
            if (ball_bottom < FLOOR_Y) {
                ball_y++;
            } else {
                /* Floor hit — lose a life */
                g_lives--;
                audio_play_sfx(SFX_LIFE_LOST);
                if (g_lives == 0) { game_over = 1; draw_game_over(); audio_play_sfx(SFX_GAME_OVER); }
                else              { reset_ball(); }
            }
        }
    }

    /* Step 2: Launch with Space (after position is set) */
    if (cpct_isKeyPressed(Key_Space) && !ball_launched) {
        ball_launched = 1;
        ball_vx = 1;
        ball_vy = -1;
    }

    /* Step 3: Paddle movement */
    if (cpct_isKeyPressed(Key_CursorLeft)  && paddle_x > 0)               paddle_x--;
    if (cpct_isKeyPressed(Key_CursorRight) && paddle_x < 80 - PADDLE_WIDTH) paddle_x++;

    /* Step 4: Paddle collision — invert ball_vy with -ball_vy, NEVER hardcode -1 */
    if (ball_launched) {
        ball_right  = ball_x + BALL_W - 1;
        ball_bottom = ball_y + BALL_H - 1;
        if (ball_vy > 0 && ball_bottom >= PADDLE_Y && ball_y <= PADDLE_Y + 1 &&
            ball_right >= paddle_x && ball_x < paddle_x + PADDLE_WIDTH) {
            ball_vy = -ball_vy;
            ball_y  = PADDLE_Y - BALL_H;
            audio_play_sfx(SFX_PADDLE_HIT);
        }
    }

    /* Step 5: Block collision — NO direction guard, check ALL blocks */
    if (ball_launched) {
        for (i = 0; i < BLOCK_ROWS; i++) {
            for (j = 0; j < BLOCK_COLS; j++) {
                if (ball_bottom >= 20 + i * BLOCK_HEIGHT &&
                    ball_y      <= 20 + i * BLOCK_HEIGHT + BLOCK_HEIGHT - 1 &&
                    ball_right  >= j * BLOCK_WIDTH &&
                    ball_x      <  j * BLOCK_WIDTH + BLOCK_WIDTH) {
                    pv = cpct_getScreenPtr(CPCT_VMEM_START, j * BLOCK_WIDTH, 20 + i * BLOCK_HEIGHT);
                    cpct_drawSolidBox(pv, 0x00, BLOCK_WIDTH, BLOCK_HEIGHT);
                    if (ball_vy < 0) ball_vy = 1; else ball_vy = -1;
                    g_score += 10;
                    audio_play_sfx(SFX_BRICK_HIT);
                }
            }
        }
    }
}

void draw_game(void) {
    u8 *pv;                        /* declared ONCE at top */

    /* Ball — erase old, draw new */
    pv = cpct_getScreenPtr(CPCT_VMEM_START, prev_ball_x, prev_ball_y);
    cpct_drawSolidBox(pv, 0x00, BALL_W, BALL_H);
    pv = cpct_getScreenPtr(CPCT_VMEM_START, ball_x, ball_y);
    cpct_drawSolidBox(pv, g_ball_color, BALL_W, BALL_H);
    prev_ball_x = ball_x; prev_ball_y = ball_y;

    /* Paddle — erase old, draw new */
    pv = cpct_getScreenPtr(CPCT_VMEM_START, prev_paddle_x, PADDLE_Y);
    cpct_drawSolidBox(pv, 0x00, PADDLE_WIDTH, 2);
    pv = cpct_getScreenPtr(CPCT_VMEM_START, paddle_x, PADDLE_Y);
    cpct_drawSolidBox(pv, g_paddle_color, PADDLE_WIDTH, 2);
    prev_paddle_x = paddle_x;
}

void main(void) {
    init_game();
    while (1) {
        cpct_scanKeyboard_f();     /* NOT cpct_scanKeyboard() */
        update_game();
        draw_game();
        cpct_waitVSYNC();
    }
}
```

---

## RULE-008: Full-Screen Clear Inside while(1) = Black Screen

**This bug has two causes that stack together:**

**Cause 1 — Performance:** At 4MHz Z80, clearing 16KB costs ~12–18ms out of a 20ms frame
(50Hz). The screen is black for 60–90% of each frame. Result: completely black display.

**Cause 2 — The RAG skeleton is the source of the bug:** Models copy `cpct_memset` from
RULE-007's `init_game()` and paste it into `draw()`. The call looks identical in both
places — only the surrounding context differs. The model cannot always distinguish
"called once at startup" from "called every frame". This is why RULE-007 labels it
explicitly and draw_game() has a comment forbidding it.

**These patterns inside while(1) all produce a black screen:**
```c
/* WRONG — any of these in draw() or anywhere inside while(1): */
cpct_memset(CPCT_VMEM_START, 0x00, 0x4000);       /* 16KB linear clear — TOO SLOW */
cpct_drawSolidBox(ptr, 0x00, 80, 200);             /* full-screen solid box — TOO SLOW */
```

**CORRECT — erase only the pixels that changed:**
```c
/* Erase entity at previous position (2×2 bytes = 4×2 pixels in Mode 0) */
pv = cpct_getScreenPtr(CPCT_VMEM_START, prev_x, prev_y);
cpct_drawSolidBox(pv, 0x00, 2, 2);   /* tiny erase: fast */
/* Draw entity at new position */
pv = cpct_getScreenPtr(CPCT_VMEM_START, new_x, new_y);
cpct_drawSolidBox(pv, 0x0F, 2, 2);   /* tiny draw: fast */
prev_x = new_x; prev_y = new_y;
```

**Rule:** `cpct_memset(CPCT_VMEM_START, ...)` appears EXACTLY ONCE in the program,
inside `init_game()`, called before `while(1)`. Every draw function uses erase/draw
per entity. Static elements (grids, backgrounds, HUD frames) are drawn once at init
and erased only when they change.

---

## RULE-009: u8 for Screen Positions, i8 Only for Signed Deltas

**Compiler warnings:** `warning 94: comparison always false`, `warning 158: overflow in implicit constant conversion`, `warning 126: unreachable code`

**Root cause:** The CPC Mode 0 screen is 160×200 pixels (80×200 bytes). Any Y position
can reach 128–199, which exceeds `i8` range (-128..127). Declaring screen coordinates
as `i8` causes silent overflow and produces code that is statically unreachable.

**WRONG — i8 cannot represent positions above 127:**
```c
i8 x, y, dx, dy;   /* grouping position and velocity in i8 is WRONG */

y = 180;            /* overflow: stored as -76 in i8 */
if (y >= 150) {     /* always false: i8 max is 127 → warning 94 + unreachable code */
```

**CORRECT — split by semantic meaning:**
```c
u8 x, y;    /* screen position: always positive — Mode 0 is 80 bytes wide, 200 lines tall */
i8 dx, dy;  /* velocity / direction: can be negative */

/* All functions receiving screen positions must use u8 parameters: */
u8 check_hit(u8 x, u8 y) { ... }   /* NOT (i8 x, i8 y) */
```

**Decision rule:**
- Can the value ever be negative? → `i8` (velocity, offset, delta)
- Is it a pixel row, byte column, or sprite position? → `u8` (always 0..199 or 0..79)

---

## RULE-010: u8 + Negative i8 = Underflow — Guard Before Subtracting

**Problem:** Adding a negative `i8` value to a `u8` position variable causes unsigned
underflow: the result wraps to 255. Any subsequent `cpct_getScreenPtr(CPCT_VMEM_START, 255, y)`
computes an address far outside the screen buffer → memory corruption → program crash.

This applies to any moving entity: player, enemy, bullet, cursor, projectile.

**WRONG — unchecked `pos += delta` causes crash when pos reaches 0:**
```c
u8 x, y;
i8 dx, dy;

x += dx;             /* if x=0 and dx=-1: x becomes 255 (u8 underflow) */
y += dy;             /* same for y */
if (x <= 0) dx = 1; /* never triggers: u8 wraps to 255, not -1 */
```

**CORRECT — branch on sign, never subtract below 0:**
```c
/* Move in X */
if (dx > 0) {
    x++;
    if (x >= MAX_X) { x = MAX_X; dx = -1; }
} else {
    if (x > 0) { x--; } else { dx = 1; }
}

/* Move in Y */
if (dy < 0) {
    if (y > 0) { y--; } else { y = 0; dy = 1; }
} else {
    y++;
}
```

**Rule:** Never write `u8_pos += i8_negative_delta` without first checking `u8_pos > 0`.
The safe pattern is: branch on sign → increment OR decrement with explicit guard.

---

## RULE-011: String Rendering Must Not Exceed Screen Width

**Problem:** `cpct_drawStringM0` renders each character as **4 bytes wide** in Mode 0
(8 pixels = 4 bytes at 2px/byte). Writing past byte 79 in a screen row goes outside
the screen buffer and corrupts adjacent memory — score display, enemy positions,
even the stack — causing crashes or corrupted game state.

This applies to ANY text rendered in Mode 0: score, lives, messages, labels.

**Formula:** `x_bytes + (char_count × 4) ≤ 80`

**WRONG — any string that overflows the right edge:**
```c
/* 20 chars × 4 = 80 bytes starting at x=10 → bytes 10..89 → CRASH */
cpct_drawStringM0("PRESS SPACE TO START", ptr_at_x10, fg, bg);

/* 15 chars × 4 = 60 bytes starting at x=25 → bytes 25..84 → CRASH */
cpct_drawStringM0("INSERT COIN HERE!", ptr_at_x25, fg, bg);
```

**CORRECT — always verify: x + len*4 ≤ 80:**
```c
/* x=0, 20 chars × 4 = 80 → fits exactly */
cpct_drawStringM0("PRESS SPACE TO START", ptr_at_x0, fg, bg);

/* x=18, 11 chars × 4 = 44 → 18+44=62 ≤ 80 ✓ */
cpct_drawStringM0("PRESS SPACE", ptr_at_x18, fg, bg);

/* x=60, 3 chars × 4 = 12 → 60+12=72 ≤ 80 ✓ — good for score/lives counters */
cpct_drawStringM0("000", ptr_at_x60, fg, bg);
```

**Quick reference — max chars by starting x:**
| x (bytes) | max chars |
|-----------|-----------|
| 0         | 20        |
| 10        | 17        |
| 20        | 15        |
| 40        | 10        |
| 60        | 5         |

---

## RULE-012: Use cpct_setPALColour per Pen — Not cpct_fw2hw/cpct_setPalette

**The simplest and most reliable palette setup:**

```c
cpct_disableFirmware();
cpct_setVideoMode(0);
cpct_setPALColour(0, HW_BLACK);
cpct_setPALColour(1, HW_BRIGHT_WHITE);
cpct_setPALColour(2, HW_BRIGHT_RED);
cpct_setPALColour(3, HW_BRIGHT_GREEN);
cpct_setBorder(HW_BLACK);
```

**DO NOT use cpct_fw2hw / cpct_setPalette.** That pattern requires converting
firmware colour indices to hardware values in an array — error-prone and unnecessary.
`cpct_setPALColour` takes hardware colour constants (HW_*) directly.

**HW_* colour constants:** `HW_BLACK`, `HW_BRIGHT_WHITE`, `HW_BRIGHT_RED`,
`HW_BRIGHT_GREEN`, `HW_BRIGHT_YELLOW`, `HW_BRIGHT_CYAN`, `HW_BRIGHT_MAGENTA`,
`HW_BLUE`, `HW_WHITE`.

---

## RULE-013: Loop Index for Decrementing Loops Must Be i8, Not u8

**Problem:** A `u8` index that decrements past 0 wraps to 255, continuing indefinitely
and writing outside array bounds → stack corruption → crash.

**WRONG — u8 wraps to 255 when decremented below 0:**
```c
void int_to_str(u8 num, char *str) {
    u8 i;              /* declared u8 */
    /* ... */
    i = 2;
    while (i >= 0) {   /* warning 94: always true for u8 */
        str[i] = '0' + (num % 10);
        num /= 10;
        i--;           /* when i=0: i-- → 255, loop continues → writes str[255]! */
    }
}
```

**CORRECT — use i8 for decrementing loop indices:**
```c
void int_to_str(u8 num, char *str) {
    i8 i;              /* i8: can go negative, loop exits at -1 */
    /* ... */
    i = 2;
    while (i >= 0) {   /* exits when i=-1 */
        str[i] = '0' + (num % 10);
        num /= 10;
        i--;           /* i8: 0 → -1, loop correctly exits */
    }
}
```

**Rule:** Use `i8` (not `u8`) for any loop index or counter that may decrement to or below 0.

---

## RULE-014: cpct_scanKeyboard() Must Be in the Main Loop — Once Per Frame

**Symptom:** Keyboard completely silent. `cpct_isKeyPressed()` always returns false.

**Root cause:** `cpct_scanKeyboard()` captures the keyboard state into an internal buffer.
`cpct_isKeyPressed()` reads from that buffer. If `cpct_scanKeyboard()` is never called,
the buffer is never updated — all keys read as not pressed, forever.

**WRONG — scanKeyboard inside a subfunction:**
```c
void update_game(void) {
    cpct_scanKeyboard();        /* ← WRONG: called from subfunction */
    if (cpct_isKeyPressed(...)) { ... }
}

void main(void) {
    while (1) {
        update_game();          /* scanKeyboard buried here */
        draw_game();
        cpct_waitVSYNC();
    }
}
```

**WRONG — scanKeyboard missing entirely:**
```c
void main(void) {
    while (1) {
        update_game();          /* no scanKeyboard anywhere */
        draw_game();
        cpct_waitVSYNC();
    }
}
```

**CORRECT — scanKeyboard_f at the top of while(1), before update and draw:**
```c
void main(void) {
    init_game();   /* cpct_disableFirmware, cpct_setVideoMode, cpct_setPALColour inside */

    while (1) {
        cpct_scanKeyboard_f();  /* ← HERE: use _f variant, once per frame */
        update_game();          /* can now call cpct_isKeyPressed() safely */
        draw_game();
        cpct_waitVSYNC();
    }
}
```

**Rule:** `cpct_scanKeyboard_f()` (fast variant) appears exactly once per frame,
at the top of `while(1)`. Use `cpct_scanKeyboard_f`, NOT `cpct_scanKeyboard()`.

---

## RULE-015: Static vs Dynamic Elements — Draw Static Once at Init

**Problem:** Redrawing all blocks and HUD labels every frame causes extreme flickering.
Each `cpct_drawSolidBox` and `cpct_drawStringM0` takes CPU cycles. Drawing 50 blocks
+ 3 text strings every frame consumes most of the 20ms budget leaving only a brief
window where elements are visible — the rest is blank. Result: severe flicker.

**Classification of elements:**
- **Static** (never move): block grid, title, HUD labels ("SCORE:", "LIVES:")
- **Semi-static** (change rarely): score digits, lives digits — update only when value changes
- **Dynamic** (move every frame): ball, paddle — erase/draw every frame

**WRONG — redraws everything every frame:**
```c
void draw_game(void) {
    for (i=0;i<ROWS;i++) for (j=0;j<COLS;j++) if (blocks[i][j]) draw_block(i,j); /* WRONG */
    cpct_drawStringM0("SCORE:", pv, ...);  /* WRONG: static label every frame */
    cpct_drawStringM0(score_str, pv, ...); /* WRONG: only needed when score changes */
}
```

**CORRECT — static elements drawn once at init, dynamic ones each frame:**
```c
void init_game(void) {
    cpct_memset(CPCT_VMEM_START, 0x00, 0x4000); /* clear once */
    for (i=0;i<ROWS;i++) for (j=0;j<COLS;j++) draw_block(i,j); /* draw ALL blocks once */
    cpct_drawStringM0("SCORE:", pv_score_label, ...); /* draw label once */
    cpct_drawStringM0("LIVES:", pv_lives_label, ...); /* draw label once */
    draw_digits();                                      /* draw initial values */
}

void update_game(void) {
    if (block_destroyed) {
        erase_block(bx, by);    /* erase only the destroyed block */
        update_score_digits();  /* redraw only digits, not the "SCORE:" label */
    }
}

void draw_game(void) {
    /* Only ball and paddle — the only elements that move */
    erase_ball_at(ball_px, ball_py);
    draw_ball_at(ball_x, ball_y);
    erase_paddle_at(paddle_px);
    draw_paddle_at(paddle_x);
}
```

---

## RULE-016: Erase and Draw of the Same Entity Must Be in the Same Function

**Problem:** If erase happens in `update_game()` and draw happens in `draw_game()`,
the entity is invisible between the two calls. At 50Hz this causes visible flickering.

**WRONG — entity invisible between update and draw:**
```c
void update_game(void) {
    cpct_drawSolidBox(old_ptr, 0x00, W, H);  /* erase here */
    ball_x += ball_vx;                        /* update */
}
void draw_game(void) {
    cpct_drawSolidBox(new_ptr, COLOR, W, H);  /* draw here — gap causes flicker */
}
```

**CORRECT — erase and draw in same function, back-to-back:**
```c
void draw_game(void) {
    /* Erase at previous position */
    pv = cpct_getScreenPtr(CPCT_VMEM_START, prev_x, prev_y);
    cpct_drawSolidBox(pv, 0x00, W, H);
    /* Draw at new position — immediately after erase */
    pv = cpct_getScreenPtr(CPCT_VMEM_START, ball_x, ball_y);
    cpct_drawSolidBox(pv, COLOR, W, H);
    prev_x = ball_x; prev_y = ball_y;  /* ← update HERE, inside draw_game */
}
```

**CRITICAL: prev_x/prev_y must be updated inside draw_game(), NEVER in update_game().**

**WRONG — updating prev in update_game() causes permanent trail on screen:**
```c
void update_game(void) {
    ball_x++;           /* move ball */
    prev_ball_x = ball_x;  /* ERROR: now prev == ball, erase hits same pixel as draw */
    prev_ball_y = ball_y;  /* → old position is NEVER erased → visible trail */
}
void draw_game(void) {
    pv = cpct_getScreenPtr(CPCT_VMEM_START, prev_ball_x, prev_ball_y);
    cpct_drawSolidBox(pv, 0x00, W, H);  /* erases NEW position, not old */
    pv = cpct_getScreenPtr(CPCT_VMEM_START, ball_x, ball_y);
    cpct_drawSolidBox(pv, COLOR, W, H); /* draws at same spot → trail grows */
}
```

---

## RULE-017: Sound Effects — Leave as Empty Stubs

DO NOT implement sound effects with `cpct_akp_SFXPlay`, `cpct_akp_MusicPlay`,
`cpct_akp_Init`, or any other `cpct_akp_*` function.

AKP sound requires pre-compiled tracker data in a specific binary format that cannot
be generated inline. Any attempt causes `error 78: incompatible types` at compile time.

**CORRECT — empty stubs compile cleanly:**
```c
void play_sound_paddle(void) {}
void play_sound_block(void)  {}
void play_sound_life(void)   {}
```


## RULE-018: Always Use cpct_px2byteM0 for Colour Bytes — Never Hardcode Them

**Symptom:** sprites or paddle render invisible (black on black). Score/HUD text
unreadable. `cpct_drawSolidBox` or `cpct_drawStringM0` called with wrong pen byte.

**Root cause:** Mode 0 pixel bytes are non-intuitive. The ONLY safe way to get the
correct byte for a pen is: `cpct_px2byteM0(pen, pen)`.

### CORRECT Mode 0 pen byte values (both pixels = pen N, with 4-entry palette)

| pen | `cpct_px2byteM0(N,N)` | use for |
|-----|------------------------|---------|
| 0   | `0x00`                | erase / background (black) |
| 1   | `0x03`                | pen 1 (e.g. white) |
| 2   | `0x0C`                | pen 2 (e.g. red) |
| 3   | `0x0F`                | pen 3 (e.g. green) |

**Common mistake — `0xC0` is pen 8, NOT pen 1. `0xCC` is pen 10, NOT pen 3.**
With a 4-entry palette, pens 4..15 are undefined → renders black → invisible sprites.

### WRONG — hardcoded wrong bytes
```c
cpct_drawSolidBox(pv, 0xC0, w, h);        /* 0xC0 = pen 8 → INVISIBLE */
cpct_drawSolidBox(pv, 0xCC, w, h);        /* 0xCC = pen 10 → INVISIBLE */
cpct_drawStringM0("SCORE", pv, 0x03, 0); /* 0x03 = pen 1, correct but fragile */
```

### CORRECT — use cpct_px2byteM0 and cpct_setPALColour
```c
/* In init_game() — palette setup */
cpct_setPALColour(0, HW_BLACK);
cpct_setPALColour(1, HW_BRIGHT_WHITE);
cpct_setPALColour(2, HW_BRIGHT_RED);
cpct_setPALColour(3, HW_BRIGHT_GREEN);

/* Colour bytes via cpct_px2byteM0 */
u8 g_ball_color   = cpct_px2byteM0(1, 1);  /* pen 1, both pixels */
u8 g_paddle_color = cpct_px2byteM0(2, 2);  /* pen 2, both pixels */
u8 g_fg_color     = cpct_px2byteM0(1, 1);  /* text foreground */

cpct_drawSolidBox(pv, g_paddle_color, PADDLE_WIDTH, 2);   /* visible */
cpct_drawSolidBox(pv, 0x00, PADDLE_WIDTH, 2);             /* erase — 0x00 always safe */
cpct_drawStringM0("SCORE", pv, g_fg_color, 0x00);         /* visible text */
```

## RULE-019: Velocity Variable Must Actually Be Used in the Movement Increment

**Symptom (BUG-008):** the ball/paddle moves visibly slower than the declared
velocity. `i8 ball_vx = 2;` is initialised to 2 but the entity moves 1 pixel
per frame, regardless.

**Cause:** the update function checks the SIGN of the velocity to choose
between `pos++` and `pos--`, but uses literal `++/--` (always 1) instead of
`pos += vx`. The velocity magnitude is silently discarded.

**WRONG:**
```c
i8 ball_vx = 2;
if (ball_vx > 0) ball_x++;   /* always +1, ignores the "2" */
else             ball_x--;
```

**CORRECT:**
```c
i8 ball_vx = 2;
ball_x += ball_vx;           /* uses the magnitude */
if (ball_x >= 159 - BALL_SIZE) { ball_x = 159 - BALL_SIZE; ball_vx = -ball_vx; }
if (ball_x <= 0)              { ball_x = 0;                ball_vx = -ball_vx; }
```

If `ball_x` is `u8` and `ball_vx` is `i8`, SDCC promotes correctly — but ALWAYS
clamp the bounds AFTER the increment, before any boundary test that could go
negative. See RULE-010 for u8 underflow protection.

## RULE-020: Never Compare `u8 < 0` — Always False, Underflow Already Happened

**Symptom (BUG-009):** SDCC warning "comparison is always false due to limited
range of data type"; paddle jumps to the opposite side of the screen when it
hits the left edge.

**Cause:**
```c
u8 paddle_x = 1;
paddle_x -= 3;          /* underflow → 254 */
if (paddle_x < 0) ...   /* false, the bug already happened */
```

**CORRECT — guard BEFORE subtracting:**
```c
if (paddle_x >= PADDLE_SPEED) paddle_x -= PADDLE_SPEED;
else                          paddle_x = 0;
```

Or use a temporary signed value:
```c
i16 new_x = (i16)paddle_x - PADDLE_SPEED;
paddle_x = (new_x < 0) ? 0 : (u8)new_x;
```

---

## RULE-021: Manual Integer-to-Digits — Never Pass an Uninitialised `char[]` to `cpct_drawStringM0`

**Symptom (BUG-010):** the HUD shows random colored garbage (Latin-1 high bytes,
broken glyphs) where a score or lives counter should be. The game runs fine,
collisions work, the number "updates" but visually it's noise.

**Cause (very common LLM mistake):**
```c
char score_str[8];                                /* declared, never written */
cpct_drawStringM0(score_str, pv, 0xC0, 0x00);     /* prints stack garbage */
```
`sprintf`, `itoa`, `cpct_itoa`, `cpct_drawHexByteM0` **DO NOT EXIST** in
CPCtelera/SDCC — they are in the FORBIDDEN list. The model must convert the
integer to ASCII digits **manually** before drawing.

**CORRECT — 3-digit zero-padded score (0..999):**
```c
char score_str[5];
score_str[0] = '0' + (g_score / 100) % 10;
score_str[1] = '0' + (g_score /  10) % 10;
score_str[2] = '0' + (g_score      ) % 10;
score_str[3] = 0;                                  /* null terminator */
cpct_drawStringM0(score_str, pv, 0xC0, 0x00);
```

**CORRECT — single digit (lives 0..9):**
```c
char lives_str[2];
lives_str[0] = '0' + g_lives;
lives_str[1] = 0;
cpct_drawStringM0(lives_str, pv, 0xC0, 0x00);
```

**ALTERNATIVE — draw the digit char directly (no buffer at all):**
```c
char buf[2]; buf[1] = 0;
buf[0] = '0' + (g_score / 100) % 10;
cpct_drawStringM0(buf, cpct_getScreenPtr(CPCT_VMEM_START, 60, 0), 0xC0, 0x00);
buf[0] = '0' + (g_score /  10) % 10;
cpct_drawStringM0(buf, cpct_getScreenPtr(CPCT_VMEM_START, 62, 0), 0xC0, 0x00);
buf[0] = '0' + (g_score      ) % 10;
cpct_drawStringM0(buf, cpct_getScreenPtr(CPCT_VMEM_START, 64, 0), 0xC0, 0x00);
```

**Reminder:** the buffer MUST have room for the null terminator (`buf[N-1] = 0`).
A 3-digit number needs `char buf[4]`, NOT `char buf[3]`.

---

## RULE-022: HUD String Layout — Each Mode 0 Char Is 4 Bytes Wide (8 pixels)

In Mode 0 each character drawn by `cpct_drawStringM0` is **8 pixels = 4 bytes**
wide (Mode 0 packs 2 pixels per byte). To place several labels in the same
screen row without overlap:

```
next_x_bytes = previous_x_bytes + 4 * strlen(previous_text)
```

Screen byte limits in Mode 0: `0 <= x <= 79`, `0 <= y <= 199`. "BREAKOUT" (8
chars) takes 32 bytes — almost half the screen. Plan accordingly.

**WRONG (strings overlap):**
```c
pv = cpct_getScreenPtr(CPCT_VMEM_START,  5, 0); cpct_drawStringM0("LIVES:3",  pv, 0xC0, 0x00); /* x  5..33 */
pv = cpct_getScreenPtr(CPCT_VMEM_START, 20, 0); cpct_drawStringM0("BREAKOUT", pv, 0xC0, 0x00); /* x 20..52  OVERLAPS LIVES */
pv = cpct_getScreenPtr(CPCT_VMEM_START, 60, 0); cpct_drawStringM0("SCORE:0",  pv, 0xC0, 0x00); /* x 60..88  OFF-SCREEN (>79) */
```

**CORRECT — one HUD row with two compact fields:**
```c
/* LIVES:N  (8 chars = 32 bytes)  → x 0..31 */
pv = cpct_getScreenPtr(CPCT_VMEM_START,  0, 0); cpct_drawStringM0(lives_str, pv, 0xC0, 0x00);
/* SCORE:NNN (9 chars = 36 bytes)  → x 36..71, leaves 8 bytes margin */
pv = cpct_getScreenPtr(CPCT_VMEM_START, 36, 0); cpct_drawStringM0(score_str, pv, 0xC0, 0x00);
/* Title "BREAKOUT" → put it on its OWN row, e.g. y=8 */
pv = cpct_getScreenPtr(CPCT_VMEM_START, 24, 8); cpct_drawStringM0("BREAKOUT", pv, 0xC0, 0x00);
```

**CORRECT — Arkanoid HUD pattern (labels once in init_game, digits updated every frame):**

LIVES: label (6 chars, with colon) is at x=0. Digit at x=24.
SCORE label (5 chars, NO colon) is at x=40. 3-digit number at x=64.
LIVES is ALWAYS on the LEFT; SCORE is ALWAYS on the RIGHT. Never swap them.

```c
/* In init_game() — draw static labels ONCE: */
pv = cpct_getScreenPtr(CPCT_VMEM_START,  0, 0);
cpct_drawStringM0("LIVES:", pv, 1, 0);          /* "LIVES:" WITH colon, x=0..23 */
pv = cpct_getScreenPtr(CPCT_VMEM_START, 24, 0);
cpct_drawStringM0("3", pv, 1, 0);               /* initial lives digit at x=24 */
pv = cpct_getScreenPtr(CPCT_VMEM_START, 40, 0);
cpct_drawStringM0("SCORE", pv, 1, 0);           /* "SCORE" NO colon, x=40..59 */
pv = cpct_getScreenPtr(CPCT_VMEM_START, 64, 0);
cpct_drawStringM0("000", pv, 1, 0);             /* initial score at x=64 */

/* draw_lives() — update digit at x=24 only: */
void draw_lives(void) {
    u8 *pv;
    char buf[2];
    buf[0] = '0' + g_lives;
    buf[1] = 0;
    pv = cpct_getScreenPtr(CPCT_VMEM_START, 24, 0);
    cpct_drawStringM0(buf, pv, 1, 0);
}

/* draw_score() — update 3-digit number at x=64 only: */
void draw_score(void) {
    u8 *pv;
    char buf[4];
    buf[0] = '0' + (g_score / 100) % 10;
    buf[1] = '0' + (g_score / 10) % 10;
    buf[2] = '0' + g_score % 10;
    buf[3] = 0;
    pv = cpct_getScreenPtr(CPCT_VMEM_START, 64, 0);
    cpct_drawStringM0(buf, pv, 1, 0);
}
```


---

## RULE-023: Global Position Variables Must NOT Have Initializers — Assign in init_game()

**Why:** In C89, global variable initializers must be constant expressions.
`u8 ball_x = paddle_x + 5` does not compile — `paddle_x` is a variable, not a constant.
The model tries to evaluate the expression manually and hardcodes a wrong number (e.g. `ball_x = 37`).

**WRONG — hardcoded magic number, wrong when paddle moves:**
```c
u8 paddle_x = 35;
u8 ball_x   = 37;           /* manual calculation, likely wrong */
u8 ball_y   = 186;          /* magic number — breaks if PADDLE_Y or BALL_H change */
```

**CORRECT — declare without initializer, assign in init_game():**
```c
u8 paddle_x;
u8 ball_x;
u8 ball_y;
u8 prev_ball_x, prev_ball_y;
u8 ball_launched;

void init_game(void) {
    paddle_x    = 35;
    ball_x      = paddle_x + (PADDLE_WIDTH >> 1) - (BALL_W >> 1); /* relative to paddle */
    ball_y      = PADDLE_Y - BALL_H - 1;
    prev_ball_x = ball_x;
    prev_ball_y = ball_y;
    ball_launched = 0;
}
```

**Rule:** Declare ALL gameplay position globals without initializers.
Assign them in `init_game()` where runtime values like `paddle_x` are available.
Any value that depends on another variable MUST be computed in a function, never as a global initializer.

---

## RULE-024: draw_* Functions Must Be Pure Draw — Never Modify Game State

**Problem:** A `draw_*` function that modifies game state variables (resets ball, changes lives,
sets flags) runs EVERY frame that function is called. If `draw_game_over()` calls `reset_ball()`,
the ball resets every frame during game over — making lives and game over undetectable.

**WRONG — game state change inside a draw function:**
```c
void draw_game_over(void) {
    u8 *pv;
    pv = cpct_getScreenPtr(CPCT_VMEM_START, 20, 100);
    cpct_drawStringM0("GAME OVER", pv, 1, 0);
    reset_ball();   /* ERROR: called every frame → game never actually ends */
    game_over = 0;  /* ERROR: immediately clears the game over flag */
}
```

**CORRECT — draw_* only calls draw functions, update_* handles state:**
```c
void draw_game_over(void) {
    u8 *pv;
    pv = cpct_getScreenPtr(CPCT_VMEM_START, 20, 100);
    cpct_drawStringM0("GAME OVER", pv, 1, 0);  /* ONLY draw */
}

/* State changes happen in update_game() or main loop: */
void update_game(void) {
    if (ball_y + BALL_H >= FLOOR_Y) {
        g_lives--;
        if (g_lives == 0) { game_over = 1; }  /* state change here */
        else               { reset_ball();     }  /* state change here */
    }
}
```

**Rule:** Every `draw_*` function contains ONLY:
- `cpct_getScreenPtr`
- `cpct_drawSolidBox`
- `cpct_drawStringM0`

It NEVER calls: `reset_ball()`, `reset_level()`, modifies `game_over`, `g_lives`, `ball_x/y`,
`ball_launched`, or any other game state variable.

---

## RULE-025: WSO2 Brick Level Map — Exact Array Values

When the game requires a WSO2-shaped brick layout, use EXACTLY this array.
The model must NOT reconstruct or improvise the pattern — copy these values verbatim.

```c
/* WSO2 brick map: 5 rows × 10 columns. 1=brick, 0=empty */
/* Columns: W(0-2)  S(3-5)  O(6-7)  2(8-9) */
u8 level_wso2[BLOCK_ROWS][BLOCK_COLS] = {
    {1, 0, 1,  1, 1, 1,  1, 1,  1, 1},   /* row 0 */
    {1, 0, 1,  1, 0, 0,  1, 0,  0, 1},   /* row 1 */
    {1, 1, 1,  1, 1, 0,  1, 0,  1, 1},   /* row 2 */
    {1, 0, 1,  0, 0, 1,  1, 0,  1, 0},   /* row 3 */
    {1, 0, 1,  1, 1, 1,  1, 1,  1, 1}    /* row 4 */
};
```

Draw only cells where level_wso2[i][j] == 1. Empty cells (0) are NOT drawn.
On level reset, restore all values to the pattern above (copy from a const backup or re-assign).


---

## RULE-027: Brick Collision — Invert ball_vy, NEVER Hardcode

When a brick is destroyed, invert the ball's y-velocity with `ball_vy = -ball_vy`.
NEVER hardcode `ball_vy = -1` (assumes ball always comes from below) or `ball_vy = 1`.

**WRONG:**
```c
block_grid[i][j] = 0;
ball_vy = -1;    /* WRONG: hardcoded direction — ball gets stuck bouncing downward */
```

**CORRECT:**
```c
block_grid[i][j] = 0;
ball_vy = -ball_vy;    /* CORRECT: invert direction */
g_score += 10;
audio_play_sfx(SFX_BRICK_HIT);
```


---

## RULE-028: reset_ball() Must Set ball_vx=1, ball_vy=-1 — NEVER 0

`reset_ball()` is called when the player loses a life. It MUST set `ball_vx = 1` and `ball_vy = -1`
so the ball is ready to re-launch. Setting them to 0 causes the ball to not move on the next launch
(the launch check sets them again, but a value of 0 causes undefined behaviour if the ball is drawn
before the next Space press).

**WRONG:**
```c
void reset_ball(void) {
    ball_x = paddle_x + (PADDLE_WIDTH - BALL_W) / 2;
    ball_y = PADDLE_Y - BALL_H;
    ball_vx = 0;    /* WRONG: ball has no direction when parked */
    ball_vy = 0;    /* WRONG */
    ball_launched = 0;
}
```

**CORRECT:**
```c
void reset_ball(void) {
    ball_x = paddle_x + (PADDLE_WIDTH - BALL_W) / 2;
    ball_y = PADDLE_Y - BALL_H;
    ball_vx = 1;    /* ready for next launch */
    ball_vy = -1;   /* ready to go up */
    ball_launched = 0;
    prev_ball_x = ball_x;
    prev_ball_y = ball_y;
}
```

Also: `init_game()` MUST assign `ball_x`, `ball_y`, `ball_vx`, `ball_vy` explicitly — never leave them as
uninitialized globals (SDCC zeroes them to 0, but 0 is an invalid velocity). Call `reset_ball()` inside
`init_game()` to set up the initial state.
