#ifndef ENTITIES_ENEMY_H
#define ENTITIES_ENEMY_H

#include <cpctelera.h>

typedef struct {
    u8 x;
    u8 y;
    i8 vx;
    i8 vy;
    u8 w;
    u8 h;
    u8 active;
} Enemy;

void enemyinit(Enemy* enemy);
void enemyupdate(Enemy* enemy);
void enemyrender(const Enemy* enemy);

#endif
