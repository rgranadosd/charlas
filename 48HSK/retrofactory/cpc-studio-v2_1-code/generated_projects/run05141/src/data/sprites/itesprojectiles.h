#ifndef SRC_DATA_SPRITES_ITESPROJECTILES_H
#define SRC_DATA_SPRITES_ITESPROJECTILES_H

#include <cpctelera.h>

typedef struct {
    u8 x;
    u8 y;
    u8 health;
} Player;

typedef struct {
    u8 x;
    u8 y;
    u8 health;
} Enemy;

typedef struct {
    u8 x;
    u8 y;
    u8 speed;
} Projectile;

extern const u8 sprites_projectiles_data[];

#endif
