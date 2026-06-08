#include <cpctelera.h>
#include "audio.h"

#define BLOCK_WIDTH 8
#define BLOCK_COLS 10
#define BLOCK_HEIGHT 8
#define BLOCK_ROWS 5
#define BALL_W 2
#define BALL_H 4
#define PADDLE_Y 190
#define PADDLE_WIDTH 10
#define FLOOR_Y 195

/* Globals */
u8 g_lives;
u8 g_score;
u8 game_over;
u8 ball_launched;
u8 blocks_remaining;
u8 paddle_x;
u8 ball_x;
u8 ball_y;
i8 ball_vx;
i8 ball_vy;
u8 prev_ball_x;
u8 prev_ball_y;
u8 prev_paddle_x;
u8 g_ball_color;
u8 g_paddle_color;
u8 block_colors[BLOCK_ROWS];
u8 block_grid[BLOCK_ROWS][BLOCK_COLS];
u8 g_pal[16];
u8 g_level;

void init_game(void);
void update_game(void);
void draw_game(void);
void draw_score(void);
void draw_lives(void);
void draw_game_over(void);
void reset_ball(void);
void reset_level(void);
void play_sound_paddle(void);
void play_sound_wall(void);
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
    u8 i, j;
    u8 *pv;
    
    g_lives = 3;
    g_score = 0;
    g_level = 1;
    game_over = 0;
    ball_launched = 0;
    blocks_remaining = BLOCK_COLS * BLOCK_ROWS;
    for (i = 0; i < BLOCK_ROWS; i++) for (j = 0; j < BLOCK_COLS; j++) block_grid[i][j] = 1;
    paddle_x = 35;
    prev_paddle_x = paddle_x;
    ball_x = paddle_x + (PADDLE_WIDTH / 2);
    ball_y = PADDLE_Y - BALL_H;
    ball_vx = 1;
    ball_vy = -1;
    prev_ball_x = ball_x;
    prev_ball_y = ball_y;

    cpct_disableFirmware();
    cpct_setVideoMode(0);
    cpct_setPALColour(0, HW_BLACK);
    cpct_setPALColour(1, HW_BRIGHT_WHITE);
    cpct_setPALColour(2, HW_BRIGHT_RED);
    cpct_setPALColour(3, HW_BRIGHT_GREEN);
    cpct_setBorder(HW_BLACK);
    cpct_clearScreen(0);

    g_ball_color = cpct_px2byteM0(1, 1);
    g_paddle_color = cpct_px2byteM0(2, 2);
    block_colors[0] = cpct_px2byteM0(2, 2);
    block_colors[1] = cpct_px2byteM0(3, 3);
    block_colors[2] = cpct_px2byteM0(1, 1);
    block_colors[3] = cpct_px2byteM0(3, 3);
    block_colors[4] = cpct_px2byteM0(2, 2);

    // Draw block grid
    for (i = 0; i < BLOCK_ROWS; i++) {
        for (j = 0; j < BLOCK_COLS; j++) {
            pv = cpct_getScreenPtr(CPCT_VMEM_START, j * BLOCK_WIDTH, 20 + i * BLOCK_HEIGHT);
            cpct_drawSolidBox(pv, block_colors[i], BLOCK_WIDTH, BLOCK_HEIGHT);
        }
    }

    // Draw 'LIVES:' label
    pv = cpct_getScreenPtr(CPCT_VMEM_START, 0, 0);
    cpct_drawStringM0("LIVES:", pv, 1, 0);

    // Draw 'SCORE' label
    pv = cpct_getScreenPtr(CPCT_VMEM_START, 40, 0);
    cpct_drawStringM0("SCORE", pv, 1, 0);

    // Draw initial paddle
    pv = cpct_getScreenPtr(CPCT_VMEM_START, paddle_x, PADDLE_Y);
    cpct_drawSolidBox(pv, g_paddle_color, PADDLE_WIDTH, 2);

    audio_init();
}

void update_game(void) {
    u8 ball_bottom;
    u8 ball_right;
    u8 *pv;
    u8 i, j;
    u8 block_x, block_y;
    u8 brick_hit = 0;

    // Handle paddle movement
    if (cpct_isKeyPressed(Key_Space) && !ball_launched) {
        ball_launched = 1;
        ball_vx = 1;
        ball_vy = -1;
    }
    if (cpct_isKeyPressed(Key_Space) && !ball_launched) {
        ball_launched = 1;
        ball_vx = 1;
        ball_vy = -1;
    }
    if (cpct_isKeyPressed(Key_CursorLeft) && paddle_x > 0) {
        paddle_x--;
    }
    if (cpct_isKeyPressed(Key_CursorRight) && paddle_x < 70) {
        paddle_x++;
    }

    // Update ball position if launched
    if (ball_launched) {
        // Update ball x position
        if (ball_vx > 0) {
            ball_x++;
            if (ball_x >= 80 - BALL_W) {
                ball_x = 80 - BALL_W;
                ball_vx = -ball_vx;
                play_sound_wall();
            }
        } else {
            if (ball_x > 0) ball_x--;
            else {
                ball_x = 0;
                ball_vx = -ball_vx;
                play_sound_wall();
            }
        }

        // Update ball y position
        if (ball_vy > 0) {
            ball_y++;
            if (ball_y >= 200 - BALL_H) {
                ball_y = 200 - BALL_H;
                ball_vy = -ball_vy;
                play_sound_wall();
            }
        } else {
            if (ball_y > 0) ball_y--;
            else {
                ball_y = 0;
                ball_vy = -ball_vy;
                play_sound_wall();
            }
        }

        // Check collisions
        ball_bottom = ball_y + BALL_H - 1;
        ball_right = ball_x + BALL_W - 1;

        // Ceiling collision
        if (ball_vy < 0 && ball_y == 0) {
            ball_vy = 1;
            play_sound_wall();
        }

        // Paddle collision
        if (ball_vy > 0 && ball_bottom >= PADDLE_Y && ball_y <= PADDLE_Y + 1 &&
            ball_right >= paddle_x && ball_x < paddle_x + PADDLE_WIDTH) {
            ball_vy = -ball_vy;
            ball_y = PADDLE_Y - BALL_H;
            play_sound_paddle();
        }

        // Brick collision
        for (i = 0; i < BLOCK_ROWS; i++) {
            for (j = 0; j < BLOCK_COLS; j++) {
                if (block_grid[i][j]) {
                    block_x = j * BLOCK_WIDTH;
                    block_y = 20 + i * BLOCK_HEIGHT;

                    if (ball_vy < 0 && ball_y <= block_y + BLOCK_HEIGHT && ball_bottom >= block_y &&
                        ball_right >= block_x && ball_x < block_x + BLOCK_WIDTH) {
                        // Top collision
                        ball_vy = -ball_vy;
                        ball_y = block_y + BLOCK_HEIGHT;
                        block_grid[i][j] = 0;
                        blocks_remaining--;
                        g_score += 10;
                        play_sound_brick();

                        // Erase the brick
                        pv = cpct_getScreenPtr(CPCT_VMEM_START, block_x, block_y);
                        cpct_drawSolidBox(pv, 0x00, BLOCK_WIDTH, BLOCK_HEIGHT);

                        brick_hit = 1;
                        goto block_done;
                    } else if (ball_vy > 0 && ball_bottom >= block_y && ball_y <= block_y + BLOCK_HEIGHT &&
                             ball_right >= block_x && ball_x < block_x + BLOCK_WIDTH) {
                        // Bottom collision
                        ball_vy = -ball_vy;
                        ball_y = block_y - BALL_H;
                        block_grid[i][j] = 0;
                        blocks_remaining--;
                        g_score += 10;
                        play_sound_brick();

                        // Erase the brick
                        pv = cpct_getScreenPtr(CPCT_VMEM_START, block_x, block_y);
                        cpct_drawSolidBox(pv, 0x00, BLOCK_WIDTH, BLOCK_HEIGHT);

                        brick_hit = 1;
                        goto block_done;
                    }
                }
            }
        }

block_done:
        // Check if all bricks are destroyed
        if (blocks_remaining == 0) {
            reset_level();
            g_level++;
        }

        // Floor collision
        if (ball_bottom >= FLOOR_Y) {
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
    } else {
        // Ball follows paddle when not launched
        ball_x = paddle_x + (PADDLE_WIDTH / 2);
        ball_y = PADDLE_Y - BALL_H;
        if (cpct_isKeyPressed(Key_Space)) {
            ball_launched = 1;
            ball_vx = 1;
            ball_vy = -1;
        }
    }
}

void draw_game(void) {
    u8 *pv;

    // Draw/erase paddle
    pv = cpct_getScreenPtr(CPCT_VMEM_START, prev_paddle_x, PADDLE_Y);
    cpct_drawSolidBox(pv, 0x00, PADDLE_WIDTH, 2);
    pv = cpct_getScreenPtr(CPCT_VMEM_START, paddle_x, PADDLE_Y);
    cpct_drawSolidBox(pv, g_paddle_color, PADDLE_WIDTH, 2);
    prev_paddle_x = paddle_x;

    // Draw/erase ball
    pv = cpct_getScreenPtr(CPCT_VMEM_START, prev_ball_x, prev_ball_y);
    cpct_drawSolidBox(pv, 0x00, BALL_W, BALL_H);
    pv = cpct_getScreenPtr(CPCT_VMEM_START, ball_x, ball_y);
    cpct_drawSolidBox(pv, g_ball_color, BALL_W, BALL_H);
    prev_ball_x = ball_x;
    prev_ball_y = ball_y;
}

void draw_score(void) {
    u8 *pv;
    char score_str[4];

    // Draw score counter
    score_str[0] = '0' + (g_score / 100) % 10;
    score_str[1] = '0' + (g_score / 10) % 10;
    score_str[2] = '0' + g_score % 10;
    score_str[3] = '\0';
    pv = cpct_getScreenPtr(CPCT_VMEM_START, 64, 0);
    cpct_drawStringM0(score_str, pv, 1, 0);
}

void draw_lives(void) {
    u8 *pv;
    char lives_str[2];

    // Draw lives counter
    lives_str[0] = '0' + g_lives;
    lives_str[1] = '\0';
    pv = cpct_getScreenPtr(CPCT_VMEM_START, 24, 0);
    cpct_drawStringM0(lives_str, pv, 1, 0);
}

void draw_game_over(void) {
    u8 *pv;

    // Draw 'GAME OVER' message
    pv = cpct_getScreenPtr(CPCT_VMEM_START, 20, 100);
    cpct_drawStringM0("GAME OVER", pv, 1, 0);
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

void reset_level(void) {
    u8 i, j;
    u8 *pv;

    // Reset block grid
    blocks_remaining = BLOCK_COLS * BLOCK_ROWS;
    for (i = 0; i < BLOCK_ROWS; i++) {
        for (j = 0; j < BLOCK_COLS; j++) {
            block_grid[i][j] = 1;
            pv = cpct_getScreenPtr(CPCT_VMEM_START, j * BLOCK_WIDTH, 20 + i * BLOCK_HEIGHT);
            cpct_drawSolidBox(pv, block_colors[i], BLOCK_WIDTH, BLOCK_HEIGHT);
        }
    }

    // Reset ball position
    reset_ball();
}

void play_sound_paddle(void) {
    audio_play_sfx(SFX_PADDLE_HIT);
}

void play_sound_wall(void) {
    audio_play_sfx(SFX_WALL_HIT);
}

void play_sound_brick(void) {
    audio_play_sfx(SFX_BRICK_HIT);
}

void play_sound_life_lost(void) {
    audio_play_sfx(SFX_LIFE_LOST);
}

void play_sound_game_over(void) {
    audio_play_sfx(SFX_GAME_OVER);
}