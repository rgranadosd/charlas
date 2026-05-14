#include "entities/enemy.h"
#include "systems/collision.h"
#include <cpctelera.h>

void enemyinit(Enemy* enemy) {
    if (!enemy) {
        return;
    }

    enemy->x = 0;
    enemy->y = 0;
    enemy->vx = 0;
    enemy->vy = 0;
    enemy->w = 4;
    enemy->h = 16;
    enemy->active = 0;
    enemy->health = 1;
    enemy->reward = 100;
}

void enemyspawn(Enemy* enemy, u8 x, u8 y, u8 move_right) {
    if (!enemy) {
        return;
    }

    enemy->x = x;
    enemy->y = y;
    enemy->vx = move_right ? 1 : -1;
    enemy->vy = 0;
    enemy->active = 1;
    enemy->health = 1;
}

void enemyupdate(Enemy* enemy) {
    i16 nextx;
    i16 nexty;

    if (!enemy || !enemy->active) {
        return;
    }

    nextx = (i16)enemy->x + (i16)enemy->vx;
    if (nextx < 2) {
        nextx = 2;
        enemy->vx = 1;
    }
    if (nextx > 74) {
        nextx = 74;
        enemy->vx = -1;
    }
    enemy->x = (u8)nextx;

    enemy->vy = (i8)(enemy->vy + 1);
    if (enemy->vy > 3) enemy->vy = 3;
    nexty = (i16)enemy->y + (i16)enemy->vy;
    nexty = collision_clamp_y_at((i16)enemy->x, nexty, enemy->h);
    enemy->y = (u8)nexty;
    if (collision_is_on_ground_at((i16)enemy->x, (i16)enemy->y, enemy->h) && enemy->vy > 0) {
        enemy->vy = 0;
    }
}

void enemyrender(const Enemy* enemy) {
    u8* pvmem;

    if (!enemy || !enemy->active) {
        return;
    }

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
    cpct_drawSolidBox(pvmem, 0x5C, enemy->w, enemy->h);
}

u8 enemydamage(Enemy* enemy, u8 damage) {
    if (!enemy || !enemy->active) {
        return 0;
    }

    if (damage >= enemy->health) {
        enemy->health = 0;
        enemy->active = 0;
        return 1;
    }

    enemy->health = (u8)(enemy->health - damage);
    return 0;
}
