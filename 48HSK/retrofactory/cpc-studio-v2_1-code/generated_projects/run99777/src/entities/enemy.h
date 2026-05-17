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
    u8 health;
    u16 reward;
    u8 kind;
} Enemy;

void enemyinit(Enemy* enemy);
void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 kind, u8 move_right);
void enemyupdate(Enemy* enemy);
void enemyrender(const Enemy* enemy);
u8 enemydamage(Enemy* enemy, u8 damage);

#endif
