#include "systems/collision.h"
#include "systems/tilemap.h"

static i16 ggroundy = 160;
static i16 gplatformy = 255;

void collision_init(void) {
    ggroundy = (i16)tilemap_ground_y();
    gplatformy = (i16)tilemap_platform_y_at(32);
}

u8 collision_is_on_ground(i16 y, u8 h) {
    return collision_is_on_ground_at(0, y, h);
}

u8 collision_is_on_ground_at(i16 x, i16 y, u8 h) {
    i16 feet;
    i16 support;

    support = (i16)tilemap_ground_y();
    gplatformy = (i16)tilemap_platform_y_at(x);
    if (gplatformy != 255 && y + (i16)h <= gplatformy + 2) {
        support = gplatformy;
    }

    feet = y + (i16)h;
    return (u8)(feet >= support);
}

i16 collision_clamp_y_to_ground(i16 y, u8 h) {
    return collision_clamp_y_at(0, y, h);
}

i16 collision_clamp_y_at(i16 x, i16 y, u8 h) {
    i16 maxy;
    i16 platformmaxy;

    ggroundy = (i16)tilemap_ground_y();
    maxy = ggroundy - (i16)h;
    gplatformy = (i16)tilemap_platform_y_at(x);
    if (gplatformy != 255) {
        platformmaxy = gplatformy - (i16)h;
        /* Only snap up if strictly below platform surface: avoids teleporting
           player who is already standing on the ground at the same y as the platform */
        if (y > platformmaxy && y < gplatformy) {
            return platformmaxy;
        }
    }

    if (y > maxy) {
        return maxy;
    }
    return y;
}

u8 collision_is_on_trap(i16 x, i16 y, u8 w, u8 h) {
    return tilemap_is_trap(x, y, w, h);
}

u8 collision_is_on_ladder(i16 x, i16 y, u8 w, u8 h) {
    return tilemap_is_ladder(x, y, w, h);
}
