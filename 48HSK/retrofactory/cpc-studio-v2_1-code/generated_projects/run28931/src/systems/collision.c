#include "systems/collision.h"
#include "systems/tilemap.h"

static i16 ggroundy = 160;

void collision_init(void) {
    ggroundy = (i16)tilemap_ground_y();
}

u8 collision_is_on_ground(i16 y, u8 h) {
    i16 feet;
    feet = y + (i16)h;
    return (u8)(feet >= ggroundy);
}

i16 collision_clamp_y_to_ground(i16 y, u8 h) {
    i16 maxy;
    maxy = ggroundy - (i16)h;
    if (y > maxy) {
        return maxy;
    }
    return y;
}
