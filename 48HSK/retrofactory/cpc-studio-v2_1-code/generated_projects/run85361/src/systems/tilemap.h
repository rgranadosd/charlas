#ifndef SYSTEMS_TILEMAP_H
#define SYSTEMS_TILEMAP_H

#include <cpctelera.h>

void tilemap_init(void);
void tilemap_render(void);
u8 tilemap_ground_y(void);
u8 tilemap_platform_y_at(i16 x);
u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h);
u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h);
u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h);
u8 tilemap_goal_x(void);

#endif
