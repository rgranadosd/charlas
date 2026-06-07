# CPCtelera / SDCC C89 Code Generation Rules

These rules apply to every worker that generates `src/main.c` for Amstrad CPC + CPCtelera.

## C89 Compliance
- Generate only C89-compatible code.
- Declare ALL local variables at the very top of the enclosing FUNCTION — not inside `for`/`while`/`switch` bodies.
- A variable declared inside a nested block (e.g. `for(...) { u8 block_color; ... }`) is a C89 violation even if it compiles by accident. Move it to the top of the function.
- Do not mix declarations and statements anywhere in the same block.

Wrong:
  for (i=0; i<ROWS; i++) { u8 block_color; /* C89 violation */ ... }

Correct:
  void my_func(void) {
      u8 i, j, block_color;   /* ALL variables declared first */
      for (i=0; i<ROWS; i++) { ... }
  }

## API discipline
- Do not invent CPCtelera or SDCC APIs.
- Use only functions that appear in the provided context or in these rules.
- If a requested change would require an unknown helper, mark status=blocked and explain.
- DO NOT use any cpct_akp_* function (cpct_akp_SFXPlay, cpct_akp_MusicPlay, cpct_akp_Init…).
  Sound data requires pre-compiled AKP tracker files that cannot be generated inline.
  Leave all sound functions as empty stubs: void play_sound_paddle(void) {}

## Screen pointer variable
- Declare `u8 *pv;` ONCE at the top of the function, before any statement.
- Use `pv = cpct_getScreenPtr(...)` (assignment only, no type prefix) everywhere else in the function.
- NEVER write `u8 *pv = cpct_getScreenPtr(...)` — it causes 'syntax error: token -> u8' in SDCC.

Correct:
  void draw_game(void) {
      u8 *pv;                          /* declared once at top */
      pv = cpct_getScreenPtr(...);     /* assignment — no u8 * prefix */
      cpct_drawSolidBox(pv, ...);
      pv = cpct_getScreenPtr(...);     /* reuse — still no u8 * prefix */
      cpct_drawSolidBox(pv, ...);
  }

## Hardware initialisation (MUST match this pattern exactly)
  cpct_disableFirmware();
  cpct_setVideoMode(0);
  cpct_setPALColour(0, HW_BLACK);
  cpct_setPALColour(1, HW_BRIGHT_WHITE);
  cpct_setPALColour(2, HW_BRIGHT_RED);
  cpct_setPALColour(3, HW_BRIGHT_GREEN);
  cpct_setBorder(HW_BRIGHT_RED);       /* diagnostic border — helps spot black-screen bugs */

- Use cpct_setPALColour(pen, HW_COLOR) per pen. Do NOT use cpct_fw2hw / cpct_setPalette.
- Valid HW_* constants: HW_BLACK, HW_BRIGHT_WHITE, HW_BRIGHT_RED, HW_BRIGHT_GREEN,
  HW_BRIGHT_YELLOW, HW_BRIGHT_CYAN, HW_BRIGHT_MAGENTA, HW_BLUE, HW_WHITE.

## Colour bytes for drawing
- Use cpct_px2byteM0(pen, pen) to get the correct Mode 0 byte for a solid colour:
    u8 g_ball_color   = cpct_px2byteM0(1, 1);   /* pen 1 on both pixels */
    u8 g_paddle_color = cpct_px2byteM0(2, 2);
    block_colors[0]   = cpct_px2byteM0(2, 2);
- Do NOT hardcode raw pixel bytes (0x03, 0x0C, 0x0F). Use cpct_px2byteM0 instead.
- Exception: erase boxes always use 0x00 (black = pen 0 on both pixels):
    cpct_drawSolidBox(pv, 0x00, W, H);  /* erase */

## Screen clearing and rendering
- Clear screen ONCE at init with: cpct_clearScreen(0);   (NOT cpct_memset inside the game loop)
- Functions called from the game loop (draw_game_over, draw_start_screen, etc.) must NOT
  call cpct_clearScreen or cpct_memset — draw only the changed elements in place.
- Static elements (block grid, HUD labels, title) drawn once at init_game() — never each frame.
- Dynamic elements (ball, paddle) use the erase/draw pattern in draw_game():
    pv = cpct_getScreenPtr(CPCT_VMEM_START, prev_x, prev_y);
    cpct_drawSolidBox(pv, 0x00, W, H);       /* erase old */
    pv = cpct_getScreenPtr(CPCT_VMEM_START, new_x, new_y);
    cpct_drawSolidBox(pv, color, W, H);      /* draw new */
    prev_x = new_x; prev_y = new_y;

## Main loop (MUST follow this structure)
  void main(void) {
      init_game();
      while (1) {
          cpct_scanKeyboard_f();
          update_game();
          draw_game();
          draw_score();
          draw_lives();
          cpct_waitVSYNC();
      }
  }

- Use cpct_scanKeyboard_f() — NOT cpct_scanKeyboard().
- cpct_waitVSYNC() at the END of the loop, always.

## Screen layout for ball games (Mode 0 = 80 bytes × 200 pixels)
  BLOCK_WIDTH=8  BLOCK_COLS=10  → 10×8=80 bytes = full screen width
  BLOCK_HEIGHT=8  BLOCK_ROWS=5  → block grid at y=20..59
  BALL_W=2  BALL_H=4
  PADDLE_Y=190   PADDLE_WIDTH=10
  FLOOR_Y=195    — MUST be > PADDLE_Y

  Required collisions — ALL four must be present:
  1. Top:    if (ball_vy < 0 && ball_y == 0) ball_vy = 1;
  2. Sides:  if (ball_right >= 79) ball_vx = -1;  /  if (ball_x == 0) ball_vx = 1;
  3. Paddle: AABB — use ball_bottom = ball_y + BALL_H - 1, ball_right = ball_x + BALL_W - 1
  4. Floor:  if (ball_bottom >= FLOOR_Y) { g_lives--; reset_ball(); }

## Type rules
- `u8` for all screen coordinates (x bytes 0-79, y pixels 0-199).
- `i8` only for signed deltas (velocity, direction).

## Code changes
- Prefer minimal patches over rewriting the whole file.
- When accumulating tasks, include ALL existing code — never drop declarations or functions.
