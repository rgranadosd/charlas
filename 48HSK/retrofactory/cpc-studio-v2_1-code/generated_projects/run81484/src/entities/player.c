#include "entities/player.h"
#include "systems/input.h"
#include "systems/collision.h"
#include "data/sprites/playerknight.h"
#include <cpctelera.h>

/* Use #define instead of `static const i8` so values are inlined as immediates.
   With --no-std-crt0 there is no GSINIT phase that copies INITIALIZER -> DATA. */
#define kplayermovespeed     2
#define kplayeracceleration  2
#define kplayerdeceleration  2
#define kplayergravity       1
#define kplayermaxfall       4
#define kplayerjumpvelocity  (-6)
#define kplayerjumpboost     (-1)
#define kplayerspritebytes   192

static u8 gplayersprite[kplayerspritebytes];
static u8 gplayerspritefacingleft;

void playerinit(Player* player) {
    u8 index;
    if (!player) {
        return;
    }

    player->x = 4;
    player->y = (u8)(104);  /* groundy(128) - h(24) = 104: feet at ground level */
    player->vx = 0;
    player->vy = 0;
    player->w = 8;
    player->h = 24;
    player->health = 3;
    player->weapon = 0;
    player->facing_left = 0;
    player->jump_hold = 0;
    for (index = 0; index < kplayerspritebytes; ++index) {
        gplayersprite[index] = sprplayerknight_data[index];
    }
    gplayerspritefacingleft = 0;
}

void playerupdate(Player* player) {
    i16 nextx;
    i16 nexty;

    if (!player) {
        return;
    }

    if (input_is_left_pressed()) {
        player->vx = (i8)(player->vx - kplayeracceleration);
        player->facing_left = 1;
    } else if (input_is_right_pressed()) {
        player->vx = (i8)(player->vx + kplayeracceleration);
        player->facing_left = 0;
    } else if (player->vx > 0) {
        player->vx = (i8)(player->vx - kplayerdeceleration);
        if (player->vx < 0) player->vx = 0;
    } else if (player->vx < 0) {
        player->vx = (i8)(player->vx + kplayerdeceleration);
        if (player->vx > 0) player->vx = 0;
    }

    if (player->vx > kplayermovespeed) player->vx = kplayermovespeed;
    if (player->vx < -kplayermovespeed) player->vx = -kplayermovespeed;

    if (input_is_jump_just_pressed() && collision_is_on_ground_at((i16)player->x, (i16)player->y, player->h)) {
        player->vy = kplayerjumpvelocity;
        player->jump_hold = 5;
    }

    if (input_is_jump_pressed() && player->jump_hold && player->vy < 0) {
        player->vy = (i8)(player->vy + kplayerjumpboost);
        player->jump_hold--;
    } else {
        player->jump_hold = 0;
    }

    player->vy = (i8)(player->vy + kplayergravity);
    if (player->vy > kplayermaxfall) player->vy = kplayermaxfall;

    nextx = (i16)player->x + (i16)player->vx;
    if (nextx < 0) {
        nextx = 0;
    }
    if (nextx > 72) {
        nextx = 72;
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
    if (player->facing_left != gplayerspritefacingleft) {
        cpct_hflipSpriteM0(player->w, player->h, gplayersprite);
        gplayerspritefacingleft = player->facing_left;
    }
    cpct_drawSprite(gplayersprite, pvmem, player->w, player->h);
}

u8 player_get_ammo(const Player* player) {
    (void)player;
    return 3;
}

u8 player_get_health(const Player* player) {
    return player ? player->health : 0;
}

u8 player_get_weapon(const Player* player) {
    return player ? player->weapon : 0;
}
