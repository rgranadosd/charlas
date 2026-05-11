#ifndef _LEVEL1_H_
#define _LEVEL1_H_

#include <cpctelera.h>

extern const u8 level1_tilemap[];
extern const u8 level1_tilemap_width;
extern const u8 level1_tilemap_height;
extern const u8 level1_palette[16];

typedef struct {
    u8 x, y;
    u8 type; // 0=player, 1=zombie, 2=skeleton, 3=ghoul, 4=imp, 5=checkpoint, 6=relic
} SpawnPoint;

extern const SpawnPoint level1_spawn_points[];
extern const u8 level1_spawn_points_count;

extern const u8 tileset[256][8];

extern const u8 font[96][8];

#endif