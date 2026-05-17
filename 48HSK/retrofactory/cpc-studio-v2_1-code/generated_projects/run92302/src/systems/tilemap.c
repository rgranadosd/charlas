#include "systems/tilemap.h"
#include "data/level1.h"
#include <cpctelera.h>

static u8 gtilegroundy = 160;
static u8 gtileplatformy = 128;
static u8 ggoalx = 72;

void tilemap_init(void) {
    if (level1tilemapheight > 2) {
        gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
    } else {
        gtilegroundy = 160;
    }
    gtileplatformy = (u8)(gtilegroundy - 24);
    ggoalx = 72;
}

void tilemap_render(void) {
    u8* pvmem;
    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
    cpct_drawSolidBox(pvmem, cpct_px2byteM0(1, 1), 80, 8);

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
    cpct_drawSolidBox(pvmem, cpct_px2byteM0(2, 2), 32, 4);

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
    cpct_drawSolidBox(pvmem, cpct_px2byteM0(3, 3), 16, 2);

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
    cpct_drawSolidBox(pvmem, cpct_px2byteM0(5, 5), 2, 16);
}

u8 tilemap_ground_y(void) {
    return gtilegroundy;
}

u8 tilemap_platform_y_at(i16 x) {
    if (x >= 24 && x <= 56) {
        return gtileplatformy;
    }
    return 255;
}

u8 tilemap_is_trap(i16 x, i16 y, u8 w, u8 h) {
    i16 left;
    i16 right;
    i16 feet;

    left = x;
    right = x + (i16)w;
    feet = y + (i16)h;

    if (feet >= (i16)gtilegroundy - 2 && left < 72 && right > 56) {
        return 1;
    }
    return 0;
}

u8 tilemap_is_ladder(i16 x, i16 y, u8 w, u8 h) {
    (void)x;
    (void)y;
    (void)w;
    (void)h;
    return 0;
}

u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
    (void)x;
    (void)y;
    (void)w;
    (void)h;
    return 0;
}

u8 tilemap_goal_x(void) {
    return ggoalx;
}
