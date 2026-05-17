#include "systems/hud.h"

static u8  currenthealth;
static u16 currentscore;
static u8  currenttime;
static u8  currentlives;
static u8  currentweapon;

/* Fallback compile-clean sprites while real HUD assets are wired. */
static const u8 _hud_dummy_sprite[64] = {0};
static const u8 hudhealth[64] = {0};
static const u8 hudlives[64]  = {0};

/* GSINIT-safe digit lookup: a function avoids initialised pointer arrays
   (those require the INITIALIZER -> DATA copy that --no-std-crt0 skips). */
static const u8* hud_get_number_sprite(u8 digit) {
    (void)digit;
    return _hud_dummy_sprite;
}

static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {
    u8 i;
    u8 digit;
    u16 divisor;
    u8* pvmem;

    divisor = 1;
    for (i = 1; i < digits; ++i) {
        divisor *= 10;
    }

    for (i = 0; i < digits; ++i) {
        digit = (u8)(value / divisor);
        value = (u16)(value % divisor);

        pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 8), y);
        cpct_drawSprite((u8*)hud_get_number_sprite(digit), pvmem, 8, 8);

        if (divisor > 1) {
            divisor /= 10;
        }
    }
}

void hudinit(void) {
    currenthealth = 3;
    currentscore  = 0;
    currenttime   = 90;
    currentlives  = 3;
    currentweapon = 0;
}

void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
    currenthealth = lives;
    currentscore  = score;
    currenttime   = time;
    currentlives  = lives;
    currentweapon = weapon;
}

void hudrender(void) {
    u8 i;
    u8* pvmem;
    u16 scoretemp;
    u8 timetemp;

    for (i = 0; i < currenthealth; ++i) {
        pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (i * 8), 2);
        cpct_drawSprite((u8*)hudhealth, pvmem, 8, 8);
    }

    scoretemp = currentscore;
    hud_draw_digits(scoretemp, 4, 24, 2);

    timetemp = currenttime;
    hud_draw_digits((u16)timetemp, 3, 56, 2);

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
    cpct_drawSprite((u8*)hudlives, pvmem, 8, 8);

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
    cpct_drawSprite((u8*)hud_get_number_sprite(currentlives % 10), pvmem, 8, 8);

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
    cpct_drawSprite((u8*)hud_get_number_sprite(currentweapon % 10), pvmem, 8, 8);
}
