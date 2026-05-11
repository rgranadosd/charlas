#ifndef _ENEMY_H_
#define _ENEMY_H_

#include <types.h>

typedef struct {
    u8 x, y;
    u8 width, height;
    i8 vx, vy;
    u8 health;
    u8 type;
    u8 state;
    u8 frame;
    u8 active;
} Enemy;

enum EnemyType {
    ENEMY_ZOMBIE,
    ENEMY_GARGOYLE,
    ENEMY_HELLHOUND
};

enum EnemyState {
    ENEMY_IDLE,
    ENEMY_WALKING,
    ENEMY_ATTACKING,
    ENEMY_DYING
};

void enemy_init(void);
void enemy_update(void);
void enemy_render(void);
void enemy_spawn(u8 type, u8 x, u8 y);
void enemy_take_damage(u8 index, u8 damage);

#endif