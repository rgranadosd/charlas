#include "hud.h"

static const u8* heart_sprite = (u8*)0x0900;
static const u8* numbers[10] = {
    (u8*)0x0920, (u8*)0x0930, (u8*)0x0940, (u8*)0x0950, (u8*)0x0960,
    (u8*)0x0970, (u8*)0x0980, (u8*)0x0990, (u8*)0x09A0, (u8*)0x09B0
};

void hud_init(void) {
    // Initialize HUD elements
}

void hud_draw(u16 score, u8 lives) {
    u8* pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 2);
    for (u8 i = 0; i < 5; i++) {
        u8 digit = (score / cpct_pow(10, 4 - i)) % 10;
        cpct_drawSpriteMasked(numbers[digit], pvmem, 4, 8);
        pvmem += 4;
    }
    
    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 190);
    cpct_drawSpriteMasked(heart_sprite, pvmem, 8, 8);
    pvmem += 8;
    
    u8 digit = lives % 10;
    cpct_drawSpriteMasked(numbers[digit], pvmem, 4, 8);
}