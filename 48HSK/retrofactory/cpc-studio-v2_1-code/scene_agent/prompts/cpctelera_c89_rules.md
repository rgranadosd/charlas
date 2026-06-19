# CPCtelera / SDCC C89 Code Generation Rules

These rules apply to every worker that generates `src/main.c` for Amstrad CPC + CPCtelera.
They are GAME-AGNOSTIC: they teach the platform (CPC/CPCtelera/C89), not any specific game.
The game's entities, layout and mechanics always come from the TASK prompt, never from here.
Identifiers in the examples (entity_*, actor_*, tile_*) are neutral and illustrative — use the
names the task asks for.

## C89 Compliance
- Generate only C89-compatible code.
- Declare ALL local variables at the very top of the enclosing FUNCTION — not inside `for`/`while`/`switch` bodies.
- A variable declared inside a nested block (e.g. `for(...) { u8 c; ... }`) is a C89 violation even if it compiles by accident. Move it to the top of the function.
- Do not mix declarations and statements anywhere in the same block.
- A `static`/`const` initialized TABLE (a level map, layout, lookup table, string-literal array) MUST be declared at FILE SCOPE (global, before any function) — NEVER inside a function body after statements. Declaring `static const char* map[...] = {...};` in the middle of `init_game()` is a fatal SDCC error (`syntax error: token -> 'static'`). Put such tables at the top of the file as globals and just read them inside the function.

Wrong:
  for (i=0; i<ROWS; i++) { u8 c; /* C89 violation */ ... }

Correct:
  void my_func(void) {
      u8 i, j, c;            /* ALL variables declared first */
      for (i=0; i<ROWS; i++) { ... }
  }

## API discipline
- Do not invent CPCtelera or SDCC APIs.
- Use only functions that appear in the provided context or in these rules.
- If a requested change would require an unknown helper, mark status=blocked and explain.
- DO NOT use any cpct_akp_* function (cpct_akp_SFXPlay, cpct_akp_MusicPlay, cpct_akp_Init…).
  Sound data requires pre-compiled AKP tracker files that cannot be generated inline.
  Leave all sound functions as empty stubs: void play_sound_event(void) {}

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

## Hardware initialisation (MUST match this pattern — every game starts here)
  cpct_disableFirmware();
  cpct_setVideoMode(0);
  cpct_setPALColour(0, HW_BLACK);
  cpct_setPALColour(1, HW_BRIGHT_WHITE);
  cpct_setPALColour(2, HW_BRIGHT_YELLOW);
  cpct_setPALColour(3, HW_BRIGHT_CYAN);
  cpct_setBorder(HW_BLACK);
  cpct_clearScreen(0);

- cpct_setVideoMode(0) is MANDATORY. Without it the program runs in the firmware's default
  Mode 1 (blue background) and Mode-0 graphics render as stripes.
- Use cpct_setPALColour(pen, HW_COLOR) per pen. Do NOT use cpct_fw2hw / cpct_setPalette.
- Valid HW_* constants: HW_BLACK, HW_BRIGHT_WHITE, HW_BRIGHT_RED, HW_BRIGHT_GREEN,
  HW_BRIGHT_YELLOW, HW_BRIGHT_CYAN, HW_BRIGHT_MAGENTA, HW_BLUE, HW_WHITE.

## Colour bytes for drawing
- Use cpct_px2byteM0(pen, pen) — SAME pen on both pixels — to get a SOLID Mode 0 colour byte:
    g_entity_color = cpct_px2byteM0(1, 1);   /* pen 1 on both pixels — solid */
    g_actor_color  = cpct_px2byteM0(2, 2);
    tile_colors[0] = cpct_px2byteM0(2, 2);
- cpct_px2byteM0(penA, penB) with penA != penB draws two different pixels → STRIPES. Use p,p for solid.
- Do NOT hardcode raw pixel bytes (0x03, 0x0C, 0x0F). Use cpct_px2byteM0 instead.
- Exception: erase boxes always use 0x00 (black = pen 0 on both pixels):
    cpct_drawSolidBox(pv, 0x00, W, H);  /* erase */

## Screen clearing and rendering
- Clear screen ONCE at init with: cpct_clearScreen(0);   (NOT cpct_memset inside the game loop)
- Functions called from the game loop (draw_game_over, draw_start_screen, etc.) must NOT
  call cpct_clearScreen or cpct_memset — draw only the changed elements in place.
- Static scenery (the playfield/level, HUD labels, title) drawn once at init_game() — never each frame.
- Dynamic elements (the moving entities) use the erase/draw pattern in draw_game():
    pv = cpct_getScreenPtr(CPCT_VMEM_START, prev_x, prev_y);
    cpct_drawSolidBox(pv, 0x00, W, H);       /* erase old */
    pv = cpct_getScreenPtr(CPCT_VMEM_START, new_x, new_y);
    cpct_drawSolidBox(pv, color, W, H);      /* draw new */
    prev_x = new_x; prev_y = new_y;          /* update prev ONLY here, after erase+draw */

## Keyboard: scan AND read
- cpct_scanKeyboard_f() only updates state; you MUST then test keys with cpct_isKeyPressed and act.
  Scanning without any cpct_isKeyPressed means input never works.
- Use cpct_scanKeyboard_f() — NOT cpct_scanKeyboard().

## Main loop (MUST follow this structure)
  void main(void) {
      init_game();
      while (1) {
          if (!game_over) {
              cpct_scanKeyboard_f();
              update_game();
              draw_game();
              update_hud();
          }
          cpct_waitVSYNC();      /* always at the END of the loop */
      }
  }

## Type rules
- `u8` for all screen coordinates (x bytes 0-79, y pixels 0-199).
- `i8` only for signed deltas (velocity, direction).

## Code changes
- Prefer minimal patches over rewriting the whole file.
- When accumulating tasks, include ALL existing code — never drop declarations or functions.
