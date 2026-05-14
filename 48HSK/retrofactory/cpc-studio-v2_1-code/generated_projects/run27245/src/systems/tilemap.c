#include "systems/tilemap.h"
#include "data/level1.h"
#include <cpctelera.h>

static u8 gtilegroundy = 160;

void tilemap_init(void) {
    if (level1tilemapheight > 2) {
        gtilegroundy = (u8)((level1tilemapheight - 2) * 8);
    } else {
        gtilegroundy = 160;
    }
}

void tilemap_render(void) {
    u8* pvmem;
    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, gtilegroundy);
    cpct_drawSolidBox(pvmem, 0x11, 80, 8);
}

u8 tilemap_ground_y(void) {
    return gtilegroundy;
}
