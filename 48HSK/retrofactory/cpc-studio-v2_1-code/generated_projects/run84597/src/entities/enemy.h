#ifndef _ENEMY_H_
#define _ENEMY_H_

#include <cpctelera.h>
#include "player.h"

typedef struct {
    i16 x, y;
    i16 vx, vy;
    u8 width, height;
    u8 type;
    u8 state;
    u8 frame;
    u8 health;
    u8 direction;
} TEnemy;

enum {
    ENEMY_TYPE_ZOMBIE,
    ENEMY_TYPE_ARCHER,
    ENEMY_TYPE_HOUND
};

enum {
    ENEMY_STATE_WALKING,
    ENEMY_STATE_ATTACKING,
    ENEMY_STATE_DYING
};

enum {
    ENEMY_DIR_RIGHT,
    ENEMY_DIR_LEFT
};

#define MAX_ENEMIES 10

void enemy_init(TEnemy* enemy, u8 type, i16 x, i16 y);
void enemy_update(TEnemy* enemy, TPlayer* player);
void enemy_draw(TEnemy* enemy);
void enemy_hit(TEnemy* enemy, u8 damage);
void enemy_update_all(TEnemy* enemies, u8* count);
void enemy_draw_all(TEnemy* enemies, u8 count);
void enemy_spawn_update(void);

#endif