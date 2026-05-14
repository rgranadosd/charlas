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
    projectile->damage = 1;
    projectile->lifetime = 0;
    projectile->weapon = 0;
}

void projectilefire(Projectile* projectile, u8 x, u8 y, i8 dir, u8 weapon) {
    if (!projectile) {
        return;
    }

    projectile->x = x;
    projectile->y = y;
    projectile->vx = dir;
    projectile->vy = 0;
    projectile->weapon = weapon;
    projectile->active = 1;

    if (weapon == 0) {
        projectile->w = 3;
        projectile->h = 2;
        projectile->damage = 1;
        projectile->lifetime = 45;
    } else {
        projectile->w = 2;
        projectile->h = 3;
        projectile->damage = 2;
        projectile->lifetime = 28;
    }
}

void projectileupdate(Projectile* projectile) {
    if (!projectile || !projectile->active) {
        return;
    }

    projectile->x = (u8)(projectile->x + projectile->vx);
    projectile->y = (u8)(projectile->y + projectile->vy);

    if (projectile->lifetime) {
        projectile->lifetime--;
    }

    if (projectile->x > 78 || projectile->lifetime == 0) {
        projectile->active = 0;
    }
}

void projectilerender(const Projectile* projectile) {
    u8* pvmem;

    if (!projectile || !projectile->active) {
        return;
    }

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
    cpct_drawSolidBox(pvmem, projectile->weapon ? 0x6B : 0x0F, projectile->w, projectile->h);
}
