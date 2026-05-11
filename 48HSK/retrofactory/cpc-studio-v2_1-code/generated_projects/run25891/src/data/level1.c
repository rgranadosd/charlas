#include "level1.h"
#include <cpctelera.h>

const u8 level1_palette[16] = {0x54, 0x44, 0x55, 0x5C, 0x58, 0x5D, 0x4C, 0x45, 
                                0x4D, 0x56, 0x46, 0x57, 0x5E, 0x40, 0x5F, 0x4E};

const u8 level1_tilemap[] = { /* RLE compressed tilemap data */ };
const u8 level1_tilemap_width = 256;
const u8 level1_tilemap_height = 25;

const SpawnPoint level1_spawn_points[] = {
    {16, 160, 0},
    {120, 160, 1},
    {200, 160, 3},
    {300, 120, 2},
    {400, 160, 1},
    {500, 80, 4},
    {600, 160, 5},
    {700, 120, 6}
};

const u8 level1_spawn_points_count = 8;

const u8 tileset[256][8] = { /* Tile data */ };
const u8 font[96][8] = { /* Font data */ };