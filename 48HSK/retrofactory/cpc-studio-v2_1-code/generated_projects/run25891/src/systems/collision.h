#ifndef _COLLISION_H_
#define _COLLISION_H_

#include <cpctelera.h>

extern const u8 collision_mask_table[256];

extern u8* tilemap;

extern u8 tilemap_width;

extern u8 tilemap_height;

u8 collision_check_tile(u8 x, u8 y, u8 width, u8 height, u8 solid_only);
u8 collision_check_entity(u8 x1, u8 y1, u8 w1, u8 h1, u8 x2, u8 y2, u8 w2, u8 h2);

#endif