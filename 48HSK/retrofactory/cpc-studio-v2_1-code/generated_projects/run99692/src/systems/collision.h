#ifndef SYSTEMS_COLLISION_H
#define SYSTEMS_COLLISION_H

#include <cpctelera.h>

void collision_init(void);
u8 collision_is_on_ground(i16 y, u8 h);
i16 collision_clamp_y_to_ground(i16 y, u8 h);

#endif
