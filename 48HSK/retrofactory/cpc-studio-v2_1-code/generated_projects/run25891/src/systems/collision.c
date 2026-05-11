#include "collision.h"
#include "../data/level1.h"
#include <cpctelera.h>

const u8 collision_mask_table[256] = { /* Mask table data */ };

u8* tilemap = 0;
u8 tilemap_width = 0;
u8 tilemap_height = 0;

u8 collision_check_tile(u8 x, u8 y, u8 width, u8 height, u8 solid_only) {
    u8 tile_x1 = x / 8;
    u8 tile_y1 = y / 8;
    u8 tile_x2 = (x + width - 1) / 8;
    u8 tile_y2 = (y + height - 1) / 8;
    
    for (u8 tx = tile_x1; tx <= tile_x2; tx++) {
        for (u8 ty = tile_y1; ty <= tile_y2; ty++) {
            if (tx < tilemap_width && ty < tilemap_height) {
                u8 tile = tilemap[ty * tilemap_width + tx];
                if (tile >= 1 && tile <= 10) {
                    return 1;
                }
                if (!solid_only && tile >= 11 && tile <= 12) {
                    return 2; // Hazard
                }
            }
        }
    }
    return 0;
}

u8 collision_check_entity(u8 x1, u8 y1, u8 w1, u8 h1, u8 x2, u8 y2, u8 w2, u8 h2) {
    return (x1 < x2 + w2 && x1 + w1 > x2 && y1 < y2 + h2 && y1 + h1 > y2);
}