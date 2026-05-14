#include "systems/tilemap.h"
#include "data/level1.h"
#include <cpctelera.h>

static u8 gtilegroundy = 160;
static u8 gtileplatformy = 128;
static u8 ggoalx = 72;
static u8 gladderx = 36;

void tilemap_init(void) {
    if (level1tilemapheight > 2) {
        gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
    } else {
        gtilegroundy = 160;
    }
    gtileplatformy = (u8)(gtilegroundy - 24);
    ggoalx = 72;
    gladderx = 36;
}

void tilemap_render(void) {
    u8* pvmem;
    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
    cpct_drawSolidBox(pvmem, 0x11, 80, 8);

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 24, gtileplatformy);
    cpct_drawSolidBox(pvmem, 0x33, 32, 4);

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, gladderx, gtileplatformy);
    cpct_drawSolidBox(pvmem, 0x4A, 2, (u8)(gtilegroundy - gtileplatformy));

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 4, 56);
    cpct_drawSolidBox(pvmem, 0x22, 14, 8);

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 56, gtilegroundy - 2);
    cpct_drawSolidBox(pvmem, 0x66, 16, 2);

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, ggoalx, gtilegroundy - 16);
    cpct_drawSolidBox(pvmem, 0x5F, 2, 16);
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
    i16 center;
    i16 top;
    i16 bottom;

    center = x + ((i16)w / 2);
    top = y;
    bottom = y + (i16)h;

    if (center >= (i16)gladderx - 1 && center <= (i16)gladderx + 3 &&
        bottom >= (i16)gtileplatformy && top <= (i16)gtilegroundy) {
        return 1;
    }
    return 0;
}

u8 tilemap_is_hidden_zone(i16 x, i16 y, u8 w, u8 h) {
    i16 left;
    i16 right;
    i16 top;
    i16 bottom;

    left = x;
    right = x + (i16)w;
    top = y;
    bottom = y + (i16)h;

    if (left < 18 && right > 4 && top < 64 && bottom > 52) {
        return 1;
    }
    return 0;
}

u8 tilemap_goal_x(void) {
    return ggoalx;
}
