#include "entities/projectile.h"
#include <cpctelera.h>

void projectileinit(Projectile* projectile) {
    if (!projectile) {
        return;
    }

    projectile->x = 0;
    projectile->y = 0;
    projectile->vx = 0;
    projectile->vy = 0;
    projectile->w = 2;
    projectile->h = 2;
    projectile->active = 0;
}

void projectileupdate(Projectile* projectile) {
    if (!projectile || !projectile->active) {
        return;
    }

    projectile->x = (u8)(projectile->x + projectile->vx);
    projectile->y = (u8)(projectile->y + projectile->vy);
}

void projectilerender(const Projectile* projectile) {
    u8* pvmem;

    if (!projectile || !projectile->active) {
        return;
    }

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
    cpct_drawSolidBox(pvmem, 0x0F, projectile->w, projectile->h);
}
