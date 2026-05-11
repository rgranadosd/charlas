#ifndef _PROJECTILE_H_
#define _PROJECTILE_H_

#include <cpctelera.h>

typedef struct {
    u8 x, y;
    i8 vx, vy;
    u8 width, height;
    u8 lifetime;
    u8 active;
    u8 is_enemy;
} Projectile;

extern Projectile projectiles[10];

extern const u8 player_dagger_sprite[16*8/8];

extern const u8 bone_arrow_sprite[16*8/8];

extern const u8 imp_fireball_sprite[8*8/8];

void projectile_init(void);
void projectile_update(void);
void projectile_draw(void);
void projectile_create(u8 x, u8 y, i8 vx, i8 vy, u8 is_enemy);

#endif