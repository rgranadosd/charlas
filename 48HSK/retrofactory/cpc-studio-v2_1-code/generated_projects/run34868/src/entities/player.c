#include "entities/player.h"
#include "systems/input.h"
#include "systems/collision.h"
#include <cpctelera.h>

#define KPLAYERMOVESPEED    3
#define KPLAYERACCELERATION 1
#define KPLAYERDECELERATION 1
#define KPLAYERGRAVITY      1
#define KPLAYERMAXFALL      4
#define KPLAYERJUMPVELOCITY (-6)
#define KPLAYERJUMPBOOST    (-1)

void playerinit(Player* player) {
    if (!player) {
        return;
    }

    player->x = 20;
    player->y = 120;
    player->vx = 0;
    player->vy = 0;
    player->w = 4;
    player->h = 16;
    player->health = 3;
    player->facing_left = 0;
    player->jump_hold = 0;
}

void playerupdate(Player* player) {
    i16 nextx;
    i16 nexty;

    if (!player) {
        return;
    }

    if (input_is_left_pressed()) {
        player->vx = (i8)(player->vx - KPLAYERACCELERATION);
        player->facing_left = 1;
    } else if (input_is_right_pressed()) {
        player->vx = (i8)(player->vx + KPLAYERACCELERATION);
        player->facing_left = 0;
    } else if (player->vx > 0) {
        player->vx = (i8)(player->vx - KPLAYERDECELERATION);
        if (player->vx < 0) player->vx = 0;
    } else if (player->vx < 0) {
        player->vx = (i8)(player->vx + KPLAYERDECELERATION);
        if (player->vx > 0) player->vx = 0;
    }

    if (player->vx > KPLAYERMOVESPEED) player->vx = KPLAYERMOVESPEED;
    if (player->vx < -KPLAYERMOVESPEED) player->vx = (i8)(-KPLAYERMOVESPEED);

    if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
        player->vy = KPLAYERJUMPVELOCITY;
        player->jump_hold = 5;
    }

    if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
        player->vy = (i8)(player->vy + KPLAYERJUMPBOOST);
        player->jump_hold--;
    } else {
        player->jump_hold = 0;
    }

    player->vy = (i8)(player->vy + KPLAYERGRAVITY);
    if (player->vy > KPLAYERMAXFALL) player->vy = KPLAYERMAXFALL;

    nextx = (i16)player->x + (i16)player->vx;
    if (nextx < 0) {
        nextx = 0;
    }
    if (nextx > 76) {
        nextx = 76;
    }
    player->x = (u8)nextx;

    nexty = (i16)player->y + (i16)player->vy;
    nexty = collision_clamp_y_at((i16)player->x, nexty, player->h);
    if (nexty < 0) {
        nexty = 0;
    }
    player->y = (u8)nexty;

    if (collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h) && player->vy > 0) {
        player->vy = 0;
    }
}

void playerrender(const Player* player) {
    u8* pvmem;

    if (!player) {
        return;
    }

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
    cpct_drawSolidBox(pvmem, cpct_px2byteM0(6, 6), player->w, player->h);
}
