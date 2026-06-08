//-----------------------------LICENSE NOTICE------------------------------------
//  This file is part of CPCtelera: An Amstrad CPC Game Engine
//  Copyright (C) 2015 ronaldo / Fremos / Cheesetea / ByteRealms (@FranGallegoBR)
//
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU Lesser General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU Lesser General Public License for more details.
//
//  You should have received a copy of the GNU Lesser General Public License
//  along with this program.  If not, see <http://www.gnu.org/licenses/>.
//------------------------------------------------------------------------------

#include <cpctelera.h>
#include "audio.h"

#define SCREEN_WIDTH_BYTES 80
#define BLOCK_WIDTH 8
#define BLOCK_HEIGHT 8
#define BLOCK_COLS 10
#define BLOCK_ROWS 5
#define BLOCK_START_Y 20
#define BALL_W 2
#define BALL_H 4
#define PADDLE_Y 190
#define PADDLE_W 10
#define PADDLE_H 2
#define FLOOR_Y 195
#define GAME_OVER_X 20
#define GAME_OVER_Y 100

u8 g_lives;
u8 g_score;
u8 g_level;
u8 game_over;
u8 ball_launched;
u8 blocks_remaining;
u8 block_grid[BLOCK_ROWS][BLOCK_COLS];
u8 paddle_x;
u8 ball_x;
u8 ball_y;
u8 prev_paddle_x;
u8 prev_ball_x;
u8 prev_ball_y;
i8 ball_vx;
i8 ball_vy;
u8 g_ball_color;
u8 g_paddle_color;
u8 block_colors[BLOCK_ROWS];

void init_game(void);
void reset_ball(void);
void reset_level(void);
void update_game(void);
void draw_game(void);
void draw_score(void);
void draw_lives(void);
void draw_game_over(void);

void main(void) {
   cpct_disableFirmware();
   init_game();

   while (1) {
      cpct_scanKeyboard_f();

      if (!game_over) {
         update_game();
         draw_game();
         draw_score();
         draw_lives();
      } else {
         draw_game_over();
      }

      audio_update();
      cpct_waitVSYNC();
   }
}

void init_game(void) {
   u8 i;
   u8 j;
   u8* pv;

   cpct_setVideoMode(0);
   cpct_setBorder(HW_BLACK);
   cpct_setPALColour(0, HW_BLACK);
   cpct_setPALColour(1, HW_BRIGHT_WHITE);
   cpct_setPALColour(2, HW_BRIGHT_RED);
   cpct_setPALColour(3, HW_BRIGHT_GREEN);
   cpct_setPALColour(4, HW_BRIGHT_BLUE);
   cpct_setPALColour(5, HW_BRIGHT_YELLOW);
   cpct_setPALColour(6, HW_BRIGHT_MAGENTA);
   cpct_clearScreen(0);

   g_ball_color = cpct_px2byteM0(1, 1);
   g_paddle_color = cpct_px2byteM0(2, 2);
   block_colors[0] = cpct_px2byteM0(2, 2);
   block_colors[1] = cpct_px2byteM0(3, 3);
   block_colors[2] = cpct_px2byteM0(4, 4);
   block_colors[3] = cpct_px2byteM0(5, 5);
   block_colors[4] = cpct_px2byteM0(6, 6);

   g_lives = 3;
   g_score = 0;
   g_level = 1;
   game_over = 0;
   ball_launched = 0;
   blocks_remaining = BLOCK_COLS * BLOCK_ROWS;
   paddle_x = 35;
   ball_x = paddle_x + (PADDLE_W / 2);
   ball_y = PADDLE_Y - BALL_H;
   ball_vx = 1;
   ball_vy = -1;
   prev_ball_x = ball_x;
   prev_ball_y = ball_y;
   prev_paddle_x = paddle_x;

   pv = cpct_getScreenPtr(CPCT_VMEM_START, 0, 0);
   cpct_drawStringM0("LIVES:", pv, 1, 0);
   pv = cpct_getScreenPtr(CPCT_VMEM_START, 40, 0);
   cpct_drawStringM0("SCORE", pv, 1, 0);

   for (i = 0; i < BLOCK_ROWS; i++) {
      for (j = 0; j < BLOCK_COLS; j++) {
         block_grid[i][j] = 1;
         pv = cpct_getScreenPtr(CPCT_VMEM_START, j * BLOCK_WIDTH, BLOCK_START_Y + (i * BLOCK_HEIGHT));
         cpct_drawSolidBox(pv, block_colors[i], BLOCK_WIDTH, BLOCK_HEIGHT);
      }
   }

   audio_init();
   draw_score();
   draw_lives();
   draw_game();
}

void reset_ball(void) {
   ball_x = paddle_x + (PADDLE_W / 2);
   ball_y = PADDLE_Y - BALL_H;
   ball_vx = 1;
   ball_vy = -1;
   ball_launched = 0;
   prev_ball_x = ball_x;
   prev_ball_y = ball_y;
}

void reset_level(void) {
   u8 i;
   u8 j;
   u8* pv;

   blocks_remaining = BLOCK_COLS * BLOCK_ROWS;

   for (i = 0; i < BLOCK_ROWS; i++) {
      for (j = 0; j < BLOCK_COLS; j++) {
         block_grid[i][j] = 1;
         pv = cpct_getScreenPtr(CPCT_VMEM_START, j * BLOCK_WIDTH, BLOCK_START_Y + (i * BLOCK_HEIGHT));
         cpct_drawSolidBox(pv, block_colors[i], BLOCK_WIDTH, BLOCK_HEIGHT);
      }
   }

   reset_ball();
}

void update_game(void) {
   u8 i;
   u8 j;
   u8* pv;
   u8 ball_right;
   u8 ball_bottom;
   u8 block_x;
   u8 block_y;

   if (cpct_isKeyPressed(Key_CursorLeft) && paddle_x > 0) {
      paddle_x--;
   }
   if (cpct_isKeyPressed(Key_CursorRight) && paddle_x < SCREEN_WIDTH_BYTES - PADDLE_W) {
      paddle_x++;
   }

   if (!ball_launched) {
      ball_x = paddle_x + (PADDLE_W / 2);
      ball_y = PADDLE_Y - BALL_H;
   }

   if (cpct_isKeyPressed(Key_Space) && !ball_launched) {
      ball_launched = 1;
   }

   if (!ball_launched) {
      return;
   }

   if (ball_vx > 0) {
      ball_x++;
      if (ball_x >= SCREEN_WIDTH_BYTES - BALL_W) {
         ball_x = SCREEN_WIDTH_BYTES - BALL_W;
         ball_vx = -ball_vx;
         audio_play_sfx(SFX_WALL_HIT);
      }
   } else {
      if (ball_x > 0) {
         ball_x--;
      } else {
         ball_x = 0;
         ball_vx = -ball_vx;
         audio_play_sfx(SFX_WALL_HIT);
      }
   }

   if (ball_vy < 0) {
      if (ball_y > 0) {
         ball_y--;
      } else {
         ball_y = 0;
         ball_vy = -ball_vy;
         audio_play_sfx(SFX_WALL_HIT);
      }
   } else {
      ball_bottom = ball_y + BALL_H - 1;
      if (ball_bottom < FLOOR_Y) {
         ball_y++;
      } else {
         g_lives--;
         audio_play_sfx(SFX_LIFE_LOST);
         if (g_lives == 0) {
            game_over = 1;
            audio_play_sfx(SFX_GAME_OVER);
         } else {
            reset_ball();
         }
         return;
      }
   }

   ball_bottom = ball_y + BALL_H - 1;
   ball_right = ball_x + BALL_W - 1;

   if (ball_vy > 0 &&
       ball_bottom >= PADDLE_Y &&
       ball_y <= PADDLE_Y + PADDLE_H - 1 &&
       ball_right >= paddle_x &&
       ball_x < paddle_x + PADDLE_W) {
      ball_vy = -ball_vy;
      ball_y = PADDLE_Y - BALL_H;
      audio_play_sfx(SFX_PADDLE_HIT);
   }

   for (i = 0; i < BLOCK_ROWS; i++) {
      for (j = 0; j < BLOCK_COLS; j++) {
         if (block_grid[i][j]) {
            block_x = j * BLOCK_WIDTH;
            block_y = BLOCK_START_Y + (i * BLOCK_HEIGHT);

            if (ball_right >= block_x &&
                ball_x < block_x + BLOCK_WIDTH &&
                ball_bottom >= block_y &&
                ball_y < block_y + BLOCK_HEIGHT) {
               block_grid[i][j] = 0;
               pv = cpct_getScreenPtr(CPCT_VMEM_START, block_x, block_y);
               cpct_drawSolidBox(pv, 0x00, BLOCK_WIDTH, BLOCK_HEIGHT);
               ball_vy = -ball_vy;
               g_score++;
               blocks_remaining--;
               audio_play_sfx(SFX_BRICK_HIT);
               goto block_done;
            }
         }
      }
   }

block_done:;

   if (blocks_remaining == 0) {
      g_level++;
      reset_level();
   }
}

void draw_game(void) {
   u8* pv;

   pv = cpct_getScreenPtr(CPCT_VMEM_START, prev_ball_x, prev_ball_y);
   cpct_drawSolidBox(pv, 0x00, BALL_W, BALL_H);
   pv = cpct_getScreenPtr(CPCT_VMEM_START, ball_x, ball_y);
   cpct_drawSolidBox(pv, g_ball_color, BALL_W, BALL_H);

   pv = cpct_getScreenPtr(CPCT_VMEM_START, prev_paddle_x, PADDLE_Y);
   cpct_drawSolidBox(pv, 0x00, PADDLE_W, PADDLE_H);
   pv = cpct_getScreenPtr(CPCT_VMEM_START, paddle_x, PADDLE_Y);
   cpct_drawSolidBox(pv, g_paddle_color, PADDLE_W, PADDLE_H);

   prev_ball_x = ball_x;
   prev_ball_y = ball_y;
   prev_paddle_x = paddle_x;
}

void draw_score(void) {
   u8* pv;
   char buf[4];

   buf[0] = '0' + ((g_score / 100) % 10);
   buf[1] = '0' + ((g_score / 10) % 10);
   buf[2] = '0' + (g_score % 10);
   buf[3] = 0;

   pv = cpct_getScreenPtr(CPCT_VMEM_START, 64, 0);
   cpct_drawStringM0(buf, pv, 1, 0);
}

void draw_lives(void) {
   u8* pv;
   char buf[2];

   buf[0] = '0' + g_lives;
   buf[1] = 0;

   pv = cpct_getScreenPtr(CPCT_VMEM_START, 24, 0);
   cpct_drawStringM0(buf, pv, 1, 0);
}

void draw_game_over(void) {
   u8* pv;

   pv = cpct_getScreenPtr(CPCT_VMEM_START, GAME_OVER_X, GAME_OVER_Y);
   cpct_drawStringM0("GAME OVER", pv, 1, 0);
}
