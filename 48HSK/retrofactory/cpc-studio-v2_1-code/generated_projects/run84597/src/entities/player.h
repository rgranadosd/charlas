#ifndef _PLAYER_H_
#define _PLAYER_H_

#include <cpctelera.h>

typedef struct {
    i16 x, y;
    i16 vx, vy;
    u8 width, height;
    u8 state;
    u8 frame;
    u8 health;
    u8 invulnerability;
    u8 direction;
    u8 attack_cooldown;
} TPlayer;

enum {
    PLAYER_STATE_IDLE,
    PLAYER_STATE_RUNNING,
    PLAYER_STATE_JUMPING,
    PLAYER_STATE_ATTACKING,
    PLAYER_STATE_HIT,
    PLAYER_STATE_DYING
};

enum {
    PLAYER_DIR_RIGHT,
    PLAYER_DIR_LEFT
};

void player_init(TPlayer* player);
void player_update(TPlayer* player);
void player_draw(TPlayer* player);
void player_hit(TPlayer* player, u8 damage);

#endif