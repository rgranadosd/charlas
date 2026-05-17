#include "entities/projectile.h"
#include <cpctelera.h>

static const u8 projectile_basic_sprite[] = {
    cpct_px2byteM0(15, 15), cpct_px2byteM0(15, 15), cpct_px2byteM0(15, 15), cpct_px2byteM0(15, 15), cpct_px2byteM0(15, 15), cpct_px2byteM0(15, 15),
};

static const u8 projectile_up_sprite[] = {
    cpct_px2byteM0(11, 11), cpct_px2byteM0(11, 11), cpct_px2byteM0(11, 11), cpct_px2byteM0(11, 11), cpct_px2byteM0(11, 11), cpct_px2byteM0(11, 11),
};

static const u8 projectile_special_sprite[] = {
    cpct_px2byteM0(5, 5), cpct_px2byteM0(5, 5), cpct_px2byteM0(5, 5), cpct_px2byteM0(5, 5), cpct_px2byteM0(5, 5), cpct_px2byteM0(5, 5), cpct_px2byteM0(5, 5), cpct_px2byteM0(5, 5),
    cpct_px2byteM0(5, 5), cpct_px2byteM0(5, 5), cpct_px2byteM0(5, 5), cpct_px2byteM0(5, 5),
};

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
    } else if (weapon == 1) {
        projectile->w = 2;
        projectile->h = 3;
        projectile->damage = 2;
        projectile->lifetime = 28;
    } else {
        projectile->w = 4;
        projectile->h = 3;
        projectile->damage = 3;
        projectile->lifetime = 56;
        projectile->vx = (i8)(dir > 0 ? 4 : -4);
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
    const u8* sprite;

    if (!projectile || !projectile->active) {
        return;
    }

    if (projectile->weapon == 0) sprite = projectile_basic_sprite;
    else if (projectile->weapon == 1) sprite = projectile_up_sprite;
    else sprite = projectile_special_sprite;

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, projectile->x, projectile->y);
    cpct_drawSprite((u8*)sprite, pvmem, projectile->w, projectile->h);
}
