#ifndef _TILEMAP_H_
#define _TILEMAP_H_

#include <types.h>

void tilemap_init(const u8* tilemap, u8 width, u8 height);
void tilemap_render(void);

u8* tilemap_get_collision_map(void);

#endif