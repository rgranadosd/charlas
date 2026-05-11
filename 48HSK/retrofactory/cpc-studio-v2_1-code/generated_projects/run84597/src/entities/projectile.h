#ifndef _PROJECTILE_H_
#define _PROJECTILE_H_

#include <cpctelera.h>

typedef struct {
    i16 x, y;
    i16 vx, vy;
    u8 width, height;
    u8 type;
    u8 lifetime;
    u8 active;
} TProjectile;

enum {
    PROJECTILE_TYPE_LANCE,
    PROJECTILE_TYPE_ARROW
};

#define MAX_PROJECTILES 10

void projectile_init(TProjectile* projectile, u8 type, i16 x, i16 y, i16 vx, i16 vy);
void projectile_update(TProjectile* projectile);
void projectile_draw(TProjectile* projectile);
void projectile_update_all(TProjectile* projectiles, u8* count);
void projectile_draw_all(TProjectile* projectiles, u8 count);

#endif