#include <cpctelera.h>
#include "player.h"

static u8 px;
static u8 py;

void player_init(void) {
    px = 20;
    py = 80;
}

void player_update(void) {
    if (cpct_isKeyPressed(Key_CursorLeft) && px > 0)
        px -= 2;

    if (cpct_isKeyPressed(Key_CursorRight) && px < 70)
        px += 2;
}

void player_render(void) {
    u8* pvmem;

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, py);
    cpct_drawSolidBox(pvmem, 0x00, 80, 8);

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, px, py);
    cpct_drawSolidBox(pvmem, 0xF0, 4, 8);
}
