#ifndef _TILEMAP_H_
#define _TILEMAP_H_

#include <cpctelera.h>

void tilemap_init(const u8* map, u8 width, u8 height);
void tilemap_draw(void);
void tilemap_draw_region(u8 x, u8 y, u8 width, u8 height);

#endif