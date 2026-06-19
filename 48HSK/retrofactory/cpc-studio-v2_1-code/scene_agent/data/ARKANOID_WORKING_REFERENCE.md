## ARKANOID_WORKING_REFERENCE — Proven correct Arkanoid implementation

This is the EXACT working code. Copy this structure. Do NOT invent a different architecture.

Critical invariants:
- g_lives and g_score are plain u8 scalars — NOT arrays, NOT char[]
- Floor check is INSIDE the else branch of `if (ball_vy < 0)` — NOT a separate if at the end
- Paddle collision: `ball_vy = -ball_vy` (invert) — NEVER hardcode -1
- Block collision: NO ball_vy direction guard — check ALL directions
- Level complete: `g_level++; reset_level();` — NEVER `game_over = 1;`
- update_game order: follows-paddle/move → launch → paddle-move → paddle-collision → block-collision
- Sound via play_sound_wall(), play_sound_paddle(), play_sound_brick(), play_sound_life_lost(), play_sound_game_over() wrappers that call audio_play_sfx()

```c
#include <cpctelera.h>
#include "audio.h"

#define BLOCK_WIDTH 8
#define BLOCK_HEIGHT 8
#define BLOCK_COLS 10
#define BLOCK_ROWS 5
#define BALL_W 2
#define BALL_H 4
#define PADDLE_Y 190
#define PADDLE_WIDTH 10
#define FLOOR_Y 195

/* Globals */
u8 g_ball_color;
u8 g_paddle_color;
u8 block_colors[BLOCK_ROWS];
u8 g_pal[4];
u8 ball_x, ball_y;
u8 prev_ball_x, prev_ball_y;
u8 paddle_x;
u8 prev_paddle_x;
i8 ball_vx, ball_vy;
u8 ball_bottom;
u8 g_lives;
u8 g_score;
u8 game_over;
u8 ball_launched;
u8 g_level;
u8 blocks_remaining;

void init_game(void);
void update_game(void);
void draw_game(void);
void draw_score(void);
void draw_lives(void);
void draw_game_over(void);
void reset_ball(void);
void reset_level(void);
void play_sound_wall(void);
void play_sound_paddle(void);
void play_sound_brick(void);
void play_sound_life_lost(void);
void play_sound_game_over(void);

void main(void) {
    init_game();
    while (1) {
        if (!game_over) {
            cpct_scanKeyboard_f();
            update_game();
            draw_game();
            draw_score();
            draw_lives();
        }
        audio_update();
        cpct_waitVSYNC();
    }
}

void init_game(void) {
    u8 i, j, *pv;
    cpct_disableFirmware();
    cpct_setVideoMode(0);
    cpct_setPALColour(0, HW_BLACK);
    cpct_setPALColour(1, HW_BRIGHT_WHITE);
    cpct_setPALColour(2, HW_BRIGHT_RED);
    cpct_setPALColour(3, HW_BRIGHT_GREEN);
    cpct_setBorder(HW_BRIGHT_RED);
    cpct_clearScreen(0);

    /* Initialize colors */
    g_ball_color = cpct_px2byteM0(1, 1);
    g_paddle_color = cpct_px2byteM0(2, 2);
    block_colors[0] = cpct_px2byteM0(2, 2);
    block_colors[1] = cpct_px2byteM0(3, 3);
    block_colors[2] = cpct_px2byteM0(1, 1);
    block_colors[3] = cpct_px2byteM0(3, 3);
    block_colors[4] = cpct_px2byteM0(2, 2);

    /* Draw block grid */
    for (i = 0; i < BLOCK_ROWS; i++) {
        for (j = 0; j < BLOCK_COLS; j++) {
            pv = cpct_getScreenPtr(CPCT_VMEM_START, j * BLOCK_WIDTH, 20 + i * BLOCK_HEIGHT);
            cpct_drawSolidBox(pv, block_colors[i], BLOCK_WIDTH, BLOCK_HEIGHT);
        }
    }

    /* Draw HUD */
    pv = cpct_getScreenPtr(CPCT_VMEM_START, 40, 0);
    cpct_drawStringM0("SCORE", pv, 1, 0);
    pv = cpct_getScreenPtr(CPCT_VMEM_START, 0, 0);
    cpct_drawStringM0("LIVES:", pv, 1, 0);

    /* Initialize game state */
    ball_x = 40;
    ball_y = 160;
    ball_vx = 1;
    ball_vy = -1;
    paddle_x = 35;
    g_lives = 3;
    g_score = 0;
    game_over = 0;
    ball_launched = 0;
    g_level = 1;
    blocks_remaining = BLOCK_COLS * BLOCK_ROWS;

    /* Initialize previous positions */
    prev_ball_x = ball_x;
    prev_ball_y = ball_y;
    prev_paddle_x = paddle_x;

    /* Initialize audio */
    audio_init();
}

void update_game(void) {
    u8 i, j, *pv;
    u8 ball_right;

    /* Ball movement */
    if (!ball_launched) {
        ball_x = paddle_x + (PADDLE_WIDTH / 2) - (BALL_W / 2);
        ball_y = PADDLE_Y - BALL_H;
    } else {
        if (ball_vx > 0) {
            if (ball_x + BALL_W - 1 < 79) ball_x++;
            else { ball_vx = -1; play_sound_wall(); }
        } else {
            if (ball_x > 0) ball_x--;
            else { ball_vx = 1; play_sound_wall(); }
        }

        if (ball_vy < 0) {
            if (ball_y > 0) ball_y--;
            else { ball_vy = 1; play_sound_wall(); }
        } else {
            ball_bottom = ball_y + BALL_H - 1;
            if (ball_bottom < FLOOR_Y) ball_y++;
            else {
                g_lives--;
                if (g_lives == 0) {
                    game_over = 1;
                    draw_game_over();
                    play_sound_game_over();
                } else {
                    reset_ball();
                    play_sound_life_lost();
                }
            }
        }
    }

    /* Launch ball with Space */
    if (cpct_isKeyPressed(Key_Space) && !ball_launched) {
        ball_launched = 1;
        ball_vx = 1;
        ball_vy = -1;
    }

    /* Paddle movement */
    if (cpct_isKeyPressed(Key_CursorLeft) && paddle_x > 0) paddle_x--;
    if (cpct_isKeyPressed(Key_CursorRight) && paddle_x < 80 - PADDLE_WIDTH) paddle_x++;

    /* Ball-paddle collision */
    if (ball_launched) {
        ball_right = ball_x + BALL_W - 1;
        ball_bottom = ball_y + BALL_H - 1;
        if (ball_vy > 0 && ball_bottom >= PADDLE_Y && ball_y <= PADDLE_Y + 1 &&
            ball_right >= paddle_x && ball_x < paddle_x + PADDLE_WIDTH) {
            ball_vy = -ball_vy;
            ball_y = PADDLE_Y - BALL_H;
            play_sound_paddle();
        }
    }

    /* Ball-block collision */
    if (ball_launched) {
        for (i = 0; i < BLOCK_ROWS; i++) {
            for (j = 0; j < BLOCK_COLS; j++) {
                if (ball_bottom >= 20 + i * BLOCK_HEIGHT && ball_y <= 20 + i * BLOCK_HEIGHT + BLOCK_HEIGHT - 1 &&
                    ball_right >= j * BLOCK_WIDTH && ball_x < j * BLOCK_WIDTH + BLOCK_WIDTH) {
                    /* Erase the block */
                    pv = cpct_getScreenPtr(CPCT_VMEM_START, j * BLOCK_WIDTH, 20 + i * BLOCK_HEIGHT);
                    cpct_drawSolidBox(pv, 0x00, BLOCK_WIDTH, BLOCK_HEIGHT);
                    /* Reverse ball direction */
                    if (ball_vy < 0) ball_vy = 1;
                    else ball_vy = -1;
                    /* Update score */
                    g_score += 10;
                    blocks_remaining--;
                    play_sound_brick();

                    /* Check if level is complete */
                    if (blocks_remaining == 0) {
                        g_level++;
                        reset_level();
                    }
                }
            }
        }
    }
}

void draw_game(void) {
    u8 *pv;

    /* Draw ball */
    pv = cpct_getScreenPtr(CPCT_VMEM_START, prev_ball_x, prev_ball_y);
    cpct_drawSolidBox(pv, 0x00, BALL_W, BALL_H);
    pv = cpct_getScreenPtr(CPCT_VMEM_START, ball_x, ball_y);
    cpct_drawSolidBox(pv, g_ball_color, BALL_W, BALL_H);
    prev_ball_x = ball_x;
    prev_ball_y = ball_y;

    /* Draw paddle */
    pv = cpct_getScreenPtr(CPCT_VMEM_START, prev_paddle_x, PADDLE_Y);
    cpct_drawSolidBox(pv, 0x00, PADDLE_WIDTH, 2);
    pv = cpct_getScreenPtr(CPCT_VMEM_START, paddle_x, PADDLE_Y);
    cpct_drawSolidBox(pv, g_paddle_color, PADDLE_WIDTH, 2);
    prev_paddle_x = paddle_x;
}

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

void draw_lives(void) {
    u8 *pv;
    char buf[2];

    buf[0] = '0' + g_lives;
    buf[1] = 0;

    pv = cpct_getScreenPtr(CPCT_VMEM_START, 24, 0);
    cpct_drawStringM0(buf, pv, 1, 0);
}

void draw_game_over(void) {
    u8 *pv;

    pv = cpct_getScreenPtr(CPCT_VMEM_START, 30, 100);
    cpct_drawStringM0("GAME OVER", pv, 1, 0);
}

void reset_ball(void) {
    ball_x = paddle_x + (PADDLE_WIDTH / 2) - (BALL_W / 2);
    ball_y = PADDLE_Y - BALL_H;
    ball_vx = 1;
    ball_vy = -1;
    ball_launched = 0;
    prev_ball_x = ball_x;
    prev_ball_y = ball_y;
}

void reset_level(void) {
    u8 i, j, *pv;

    /* Reset ball */
    reset_ball();

    /* Redraw all blocks */
    for (i = 0; i < BLOCK_ROWS; i++) {
        for (j = 0; j < BLOCK_COLS; j++) {
            pv = cpct_getScreenPtr(CPCT_VMEM_START, j * BLOCK_WIDTH, 20 + i * BLOCK_HEIGHT);
            cpct_drawSolidBox(pv, block_colors[i], BLOCK_WIDTH, BLOCK_HEIGHT);
        }
    }

    /* Reset blocks remaining counter */
    blocks_remaining = BLOCK_COLS * BLOCK_ROWS;
}

/* Sound stubs */
void play_sound_wall(void) { audio_play_sfx(SFX_WALL_HIT); }
void play_sound_paddle(void) { audio_play_sfx(SFX_PADDLE_HIT); }
void play_sound_brick(void) { audio_play_sfx(SFX_BRICK_HIT); }
void play_sound_life_lost(void) { audio_play_sfx(SFX_LIFE_LOST); }
void play_sound_game_over(void) { audio_play_sfx(SFX_GAME_OVER); }
```
