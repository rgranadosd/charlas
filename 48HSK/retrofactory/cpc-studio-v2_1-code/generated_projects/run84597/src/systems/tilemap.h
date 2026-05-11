#ifndef _TILEMAP_H_
#define _TILEMAP_H_

#include <cpctelera.h>

void tilemap_init(void);
u8 tilemap_get_collision(u8 x, u8 y);
void tilemap_draw(void);

#endif