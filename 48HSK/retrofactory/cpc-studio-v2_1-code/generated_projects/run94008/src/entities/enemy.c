#include "entities/enemy.h"
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
}

void enemyupdate(Enemy* enemy) {
    if (!enemy || !enemy->active) {
        return;
    }

    enemy->x = (u8)(enemy->x + enemy->vx);
    enemy->y = (u8)(enemy->y + enemy->vy);
}

void enemyrender(const Enemy* enemy) {
    u8* pvmem;

    if (!enemy || !enemy->active) {
        return;
    }

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, enemy->x, enemy->y);
    cpct_drawSolidBox(pvmem, 0x5C, enemy->w, enemy->h);
}
