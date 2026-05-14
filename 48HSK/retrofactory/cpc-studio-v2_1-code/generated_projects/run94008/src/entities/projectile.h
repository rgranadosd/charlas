#ifndef ENTITIES_PROJECTILE_H
#define ENTITIES_PROJECTILE_H

#include <cpctelera.h>

typedef struct {
    u8 x;
    u8 y;
    i8 vx;
    i8 vy;
    u8 w;
    u8 h;
    u8 active;
} Projectile;

void projectileinit(Projectile* projectile);
void projectileupdate(Projectile* projectile);
void projectilerender(const Projectile* projectile);

#endif
