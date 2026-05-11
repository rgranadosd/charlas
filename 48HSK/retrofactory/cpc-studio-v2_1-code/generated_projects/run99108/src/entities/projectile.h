#ifndef _PROJECTILE_H_
#define _PROJECTILE_H_

#include <types.h>

typedef struct {
    u8 x, y;
    i8 vx, vy;
    u8 width, height;
    u8 type;
    u8 active;
    u8 range;
} Projectile;

enum ProjectileType {
    PROJECTILE_LANCE,
    PROJECTILE_DAGGER,
    PROJECTILE_FIREBALL,
    PROJECTILE_ENEMY_ARROW
};

void projectile_init(void);
void projectile_update(void);
void projectile_render(void);
void projectile_create(u8 x, u8 y, i8 vx, i8 vy, u8 type);

#endif