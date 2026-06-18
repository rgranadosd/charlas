#include <cpctelera.h>
#include "audio.h"

/* Constants */
#define BLOCK_WIDTH     8
#define BLOCK_HEIGHT    8
#define PADDLE_Y        190
#define PADDLE_WIDTH    10
#define PADDLE_HEIGHT   6
#define BALL_W          2
#define BALL_H          4
#define FLOOR_Y         195
#define PADDLE_STEP     1

/* Global state variables */
u8 g_lives;
u16 g_score;
u8 game_over;
u8 ball_launched;
u8 blocks_remaining;
u8 block_grid[5][10];
u8 paddle_x;
u8 ball_x;
u8 ball_y;
i8 ball_vx;
i8 ball_vy;
u8 prev_ball_x;
u8 prev_ball_y;
u8 prev_paddle_x;
u8 prev_lives;
u16 prev_score;
u8 game_over_drawn;

/* Colour bytes */
u8 g_paddle_color;
u8 g_ball_color;
u8 g_block_colors[5];
u8 g_hud_color;

/* HUD buffers */
char lives_buf[2] = {0};
char score_buf[4] = {0};

/* Function prototypes */
void init_game(void);
void reset_ball(void);
void update_hud(void);
void erase_brick(u8 i, u8 j);
u8 aabb_check(u8 x1, u8 y1, u8 w1, u8 h1, u8 x2, u8 y2, u8 w2, u8 h2);
void update_ball_physics(void);
void update_game(void);
void draw_game(void);
void draw_brick_grid(void);
void check_level_progression(void);
void draw_game_over(void);

/* Main function */
void main(void) {
    init_game();
    while (1) {
        cpct_waitVSYNC();
        cpct_scanKeyboard_f();

        if (!game_over) {
            update_game();
            update_ball_physics();
            check_level_progression();
        }

        draw_game();
        update_hud();

        if (game_over && !game_over_drawn) {
            draw_game_over();
            game_over_drawn = 1;
        }

        audio_update();
    }
}

void init_game(void) {
    /* Initialize state variables */
    u8 i, j;
    u8 *pv;
    u8 x, y;
    g_lives = 3;
    g_score = 0;
    game_over = 0;
    ball_launched = 0;
    blocks_remaining = 50;
    paddle_x = 35;
    prev_paddle_x = 35;
    ball_x = paddle_x + (PADDLE_WIDTH / 2);
    ball_y = PADDLE_Y - BALL_H;
    ball_vx = 1;
    ball_vy = -1;
    prev_ball_x = ball_x;
    prev_ball_y = ball_y;
    prev_lives = g_lives;
    prev_score = g_score;
    game_over_drawn = 0;

    /* Initialize block grid */
    for (i = 0; i < 5; i++) {
        for (j = 0; j < 10; j++) {
            block_grid[i][j] = 1;
        }
    }

    /* Initialize colour bytes */
    g_paddle_color = cpct_px2byteM0(1, 1);
    g_ball_color = cpct_px2byteM0(2, 2);
    g_block_colors[0] = cpct_px2byteM0(1, 1);
    g_block_colors[1] = cpct_px2byteM0(2, 2);
    g_block_colors[2] = cpct_px2byteM0(3, 3);
    g_block_colors[3] = cpct_px2byteM0(4, 4);
    g_block_colors[4] = cpct_px2byteM0(5, 5);
    g_hud_color = cpct_px2byteM0(1, 1);

    /* Hardware initialization */
    cpct_disableFirmware();
    cpct_setVideoMode(0);
    cpct_setPALColour(0, HW_BLACK);
    cpct_setPALColour(1, HW_BRIGHT_RED);
    cpct_setPALColour(2, HW_BRIGHT_YELLOW);
    cpct_setPALColour(3, HW_BRIGHT_GREEN);
    cpct_setPALColour(4, HW_BRIGHT_CYAN);
    cpct_setPALColour(5, HW_BRIGHT_BLUE);
    cpct_setBorder(HW_BLACK);
    cpct_clearScreen(0);

    /* Draw initial screen */

    /* Draw HUD labels */
    pv = cpct_getScreenPtr(CPCT_VMEM_START, 0, 0);
    cpct_drawStringM0("LIVES:", pv, 1, 0);
    pv = cpct_getScreenPtr(CPCT_VMEM_START, 40, 0);
    cpct_drawStringM0("SCORE", pv, 1, 0);

    /* Draw initial HUD values */
    lives_buf[0] = '0' + g_lives;
    lives_buf[1] = 0;
    pv = cpct_getScreenPtr(CPCT_VMEM_START, 24, 0);
    cpct_drawStringM0(lives_buf, pv, 1, 0);

    score_buf[0] = '0' + (g_score / 100) % 10;
    score_buf[1] = '0' + (g_score / 10) % 10;
    score_buf[2] = '0' + g_score % 10;
    score_buf[3] = 0;
    pv = cpct_getScreenPtr(CPCT_VMEM_START, 64, 0);
    cpct_drawStringM0(score_buf, pv, 1, 0);

    /* Draw brick grid */
    draw_brick_grid();

    /* Draw paddle */
    pv = cpct_getScreenPtr(CPCT_VMEM_START, paddle_x, PADDLE_Y);
    cpct_drawSolidBox(pv, g_paddle_color, PADDLE_WIDTH, PADDLE_HEIGHT);

    /* Draw ball */
    pv = cpct_getScreenPtr(CPCT_VMEM_START, ball_x, ball_y);
    cpct_drawSolidBox(pv, g_ball_color, BALL_W, BALL_H);

    /* Initialize audio */
    audio_init();
}

void reset_ball(void) {
    ball_x = paddle_x + (PADDLE_WIDTH / 2);
    ball_y = PADDLE_Y - BALL_H;
    ball_vx = 1;
    ball_vy = -1;
    ball_launched = 0;
    prev_ball_x = ball_x;
    prev_ball_y = ball_y;
}

void update_hud(void) {
    u8 *pv;

    /* Update lives digit if changed */
    if (g_lives != prev_lives) {
        lives_buf[0] = '0' + g_lives;
        lives_buf[1] = 0;
        pv = cpct_getScreenPtr(CPCT_VMEM_START, 24, 0);
        cpct_drawStringM0(lives_buf, pv, 1, 0);
        prev_lives = g_lives;
    }

    /* Update score digits if changed */
    if (g_score != prev_score) {
        score_buf[0] = '0' + (g_score / 100) % 10;
        score_buf[1] = '0' + (g_score / 10) % 10;
        score_buf[2] = '0' + g_score % 10;
        score_buf[3] = 0;
        pv = cpct_getScreenPtr(CPCT_VMEM_START, 64, 0);
        cpct_drawStringM0(score_buf, pv, 1, 0);
        prev_score = g_score;
    }
}

void erase_brick(u8 i, u8 j) {
    u8 *pv;
    u8 x, y;

    x = j * BLOCK_WIDTH;
    y = 20 + i * BLOCK_HEIGHT;
    pv = cpct_getScreenPtr(CPCT_VMEM_START, x, y);
    cpct_drawSolidBox(pv, 0x00, BLOCK_WIDTH, BLOCK_HEIGHT);
}

u8 aabb_check(u8 x1, u8 y1, u8 w1, u8 h1, u8 x2, u8 y2, u8 w2, u8 h2) {
    return (x1 < x2 + w2) && (x1 + w1 > x2) && (y1 < y2 + h2) && (y1 + h1 > y2);
}

void update_ball_physics(void) {
    u8 i, j;
    u8 ball_bottom;

    if (!ball_launched) return;

    // Side walls
    if (ball_vx > 0 && ball_x >= 80 - BALL_W) {
        ball_vx = -ball_vx;
        audio_play_sfx(SFX_WALL_HIT);
    } else if (ball_vx < 0 && ball_x <= 0) {
        ball_vx = -ball_vx;
        audio_play_sfx(SFX_WALL_HIT);
    }

    // Ceiling
    if (ball_vy < 0 && ball_y <= 8) {
        ball_y = 8;
        ball_vy = -ball_vy;
        audio_play_sfx(SFX_WALL_HIT);
    }

    // Floor
    if (ball_vy > 0) {
        ball_bottom = ball_y + BALL_H - 1;
        if (ball_bottom >= FLOOR_Y) {
            g_lives--;
            audio_play_sfx(SFX_LIFE_LOST);
            if (g_lives > 0) {
                reset_ball();
            } else {
                game_over = 1;
                audio_play_sfx(SFX_GAME_OVER);
            }
            return;
        }
    }

    // Paddle collision
    if (ball_vy > 0 && aabb_check(ball_x, ball_y, BALL_W, BALL_H, paddle_x, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)) {
        ball_vy = -ball_vy;
        ball_y = PADDLE_Y - BALL_H;
        audio_play_sfx(SFX_PADDLE_HIT);
    }

    // Brick collision
    for (i = 0; i < 5; i++) {
        for (j = 0; j < 10; j++) {
            if (block_grid[i][j] && aabb_check(ball_x, ball_y, BALL_W, BALL_H, j * BLOCK_WIDTH, 20 + i * BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT)) {
                block_grid[i][j] = 0;
                blocks_remaining--;
                g_score += 10;
                ball_vy = -ball_vy;
                erase_brick(i, j);
                audio_play_sfx(SFX_BRICK_HIT);
                goto block_done;
            }
        }
    }
    block_done:;
}

void update_game(void) {
    /* Update paddle position */
    if (cpct_isKeyPressed(Key_CursorLeft) && paddle_x >= PADDLE_STEP) {
        paddle_x -= PADDLE_STEP;
    }
    if (cpct_isKeyPressed(Key_CursorRight) && paddle_x + PADDLE_STEP <= 80 - PADDLE_WIDTH) {
        paddle_x += PADDLE_STEP;
    }

    /* Update ball position if launched */
    if (ball_launched) {
        /* Ball movement logic */
        if (ball_vx > 0) {
            if (ball_x + BALL_W + ball_vx <= 80) {
                ball_x += ball_vx;
            } else {
                ball_x = 80 - BALL_W;
                ball_vx = -ball_vx;
                audio_play_sfx(SFX_WALL_HIT);
            }
        } else {
            if (ball_x >= ball_vx) {
                ball_x += ball_vx;
            } else {
                ball_x = 0;
                ball_vx = -ball_vx;
                audio_play_sfx(SFX_WALL_HIT);
            }
        }

        if (ball_vy > 0) {
            if (ball_y + BALL_H + ball_vy <= FLOOR_Y) {
                ball_y += ball_vy;
            } else {
                /* Ball hits floor */
                g_lives--;
                if (g_lives == 0) {
                    game_over = 1;
                    audio_play_sfx(SFX_GAME_OVER);
                } else {
                    reset_ball();
                    audio_play_sfx(SFX_LIFE_LOST);
                }
            }
        } else {
            if (ball_y >= ball_vy) {
                ball_y += ball_vy;
            } else {
                ball_y = 0;
                ball_vy = -ball_vy;
                audio_play_sfx(SFX_WALL_HIT);
            }
        }
    } else {
        /* Ball follows paddle if not launched */
        ball_x = paddle_x + (PADDLE_WIDTH / 2);
        ball_y = PADDLE_Y - BALL_H;
        prev_ball_x = ball_x;
        prev_ball_y = ball_y;

        /* Launch ball with Space */
        if (cpct_isKeyPressed(Key_Space)) {
            ball_launched = 1;
        }
    }
}

void draw_game(void) {
    u8 *pv;

    /* Draw paddle */
    pv = cpct_getScreenPtr(CPCT_VMEM_START, prev_paddle_x, PADDLE_Y);
    cpct_drawSolidBox(pv, 0x00, PADDLE_WIDTH, PADDLE_HEIGHT);
    pv = cpct_getScreenPtr(CPCT_VMEM_START, paddle_x, PADDLE_Y);
    cpct_drawSolidBox(pv, g_paddle_color, PADDLE_WIDTH, PADDLE_HEIGHT);
    prev_paddle_x = paddle_x;

    /* Draw ball */
    pv = cpct_getScreenPtr(CPCT_VMEM_START, prev_ball_x, prev_ball_y);
    cpct_drawSolidBox(pv, 0x00, BALL_W, BALL_H);
    pv = cpct_getScreenPtr(CPCT_VMEM_START, ball_x, ball_y);
    cpct_drawSolidBox(pv, g_ball_color, BALL_W, BALL_H);
    prev_ball_x = ball_x;
    prev_ball_y = ball_y;
}

void draw_brick_grid(void) {
    u8 i, j;
    u8 *pv;
    u8 x, y;

    for (i = 0; i < 5; i++) {
        for (j = 0; j < 10; j++) {
            if (block_grid[i][j]) {
                x = j * BLOCK_WIDTH;
                y = 20 + i * BLOCK_HEIGHT;
                pv = cpct_getScreenPtr(CPCT_VMEM_START, x, y);
                cpct_drawSolidBox(pv, g_block_colors[i], BLOCK_WIDTH - 1, BLOCK_HEIGHT - 1);
            }
        }
    }
}

void check_level_progression(void) {
    u8 i, j;

    if (blocks_remaining == 0) {
        for (i = 0; i < 5; i++) {
            for (j = 0; j < 10; j++) {
                block_grid[i][j] = 1;
            }
        }
        blocks_remaining = 50;
        draw_brick_grid();
        reset_ball();
    }
}

void draw_game_over(void) {
    u8 *pv;
    pv = cpct_getScreenPtr(CPCT_VMEM_START, 30, 100);
    cpct_drawStringM0("GAME OVER", pv, 1, 0);
}