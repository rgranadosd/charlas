#include "entities/player.h"
#include "systems/input.h"
#include "systems/collision.h"
#include <cpctelera.h>

static const i8 kplayermovespeed = 2;
static const i8 kplayergravity = 1;
static const i8 kplayerjumpvelocity = -5;

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
}

void playerupdate(Player* player) {
    i16 nextx;
    i16 nexty;

    if (!player) {
        return;
    }

    player->vx = 0;
    if (input_is_left_pressed()) {
        player->vx = (i8)(-kplayermovespeed);
    } else if (input_is_right_pressed()) {
        player->vx = kplayermovespeed;
    }

    if (input_is_jump_pressed() && collision_is_on_ground((i16)player->y, player->h)) {
        player->vy = kplayerjumpvelocity;
    }

    player->vy = (i8)(player->vy + kplayergravity);

    nextx = (i16)player->x + (i16)player->vx;
    if (nextx < 0) {
        nextx = 0;
    }
    if (nextx > 76) {
        nextx = 76;
    }
    player->x = (u8)nextx;

    nexty = (i16)player->y + (i16)player->vy;
    nexty = collision_clamp_y_to_ground(nexty, player->h);
    if (nexty < 0) {
        nexty = 0;
    }
    player->y = (u8)nexty;

    if (collision_is_on_ground((i16)player->y, player->h) && player->vy > 0) {
        player->vy = 0;
    }
}

void playerrender(const Player* player) {
    u8* pvmem;

    if (!player) {
        return;
    }

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, player->x, player->y);
    cpct_drawSolidBox(pvmem, 0x4F, player->w, player->h);
}
