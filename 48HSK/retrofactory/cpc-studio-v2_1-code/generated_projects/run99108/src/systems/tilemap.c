#include "tilemap.h"
#include <cpctelera.h>

static const u8* current_tilemap;
static u8 tilemap_width;
static u8 tilemap_height;
static u8* collision_map;
static u8 camera_x = 0;

void tilemap_init(const u8* tilemap, u8 width, u8 height) {
    current_tilemap = tilemap;
    tilemap_width = width;
    tilemap_height = height;
    collision_map = cpct_malloc(width * height);
    
    for (u8 y = 0; y < height; y++) {
        for (u8 x = 0; x < width; x++) {
            u8 tile = tilemap[y * width + x];
            collision_map[y * width + x] = (tile == 1 || tile == 2) ? 1 : 0;
        }
    }
}

void tilemap_render(void) {
    u8 start_x = camera_x >> 3;
    u8 offset_x = camera_x & 7;
    
    for (u8 y = 0; y < 25; y++) {
        for (u8 x = 0; x < 21; x++) {
            u8 tile_x = start_x + x;
            if (tile_x < tilemap_width) {
                u8 tile = current_tilemap[y * tilemap_width + tile_x];
                u8* pvmem = cpct_getScreenPtr(CPCT_VMEM_START, x << 3, y << 3);
                cpct_drawTileAligned2x8_f(tilemap_tiles[tile], pvmem);
            }
        }
    }
}

u8* tilemap_get_collision_map(void) {
    return collision_map;
}