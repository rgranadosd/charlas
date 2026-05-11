#include "tilemap.h"
#include "collision.h"
#include <cpctelera.h>

const u8* current_tilemap;
u8 camera_x = 0;
u8 camera_y = 0;

extern const u8 tileset[256][8];

void tilemap_init(const u8* map, u8 width, u8 height) {
    current_tilemap = map;
    tilemap = (u8*)map;
    tilemap_width = width;
    tilemap_height = height;
    camera_x = 0;
    camera_y = 0;
}

void tilemap_draw(void) {
    u8 start_x = camera_x / 8;
    u8 start_y = camera_y / 8;
    u8 end_x = start_x + 20;
    u8 end_y = start_y + 25;
    
    if (end_x > tilemap_width) end_x = tilemap_width;
    if (end_y > tilemap_height) end_y = tilemap_height;
    
    for (u8 y = start_y; y < end_y; y++) {
        for (u8 x = start_x; x < end_x; x++) {
            u8 tile = current_tilemap[y * tilemap_width + x];
            cpct_drawTileAligned2x8_f(tileset[tile], cpct_getScreenPtr(CPCT_VMEM_START, (x - start_x) * 8, (y - start_y) * 8));
        }
    }
}