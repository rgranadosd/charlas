#include "hud.h"
#include "../entities/player.h"
#include <cpctelera.h>

static u16 score = 0;
static u8 health = 3;
static u8 lives = 3;

void hud_init(void) {
    score = 0;
    health = 3;
    lives = 3;
}

void hud_update_score(u16 points) {
    score += points;
}

void hud_update_health(u8 h) {
    health = h;
}

void hud_update_lives(u8 l) {
    lives = l;
}

void hud_render(void) {
    u8* pvmem;
    
    // Score
    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 0, 0);
    cpct_drawStringM0("SCORE:", pvmem, 6, 0);
    
    char score_str[7];
    cpct_itoa(score, score_str, 6);
    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 48, 0);
    cpct_drawStringM0(score_str, pvmem, 6, 0);
    
    // Health
    for (u8 i = 0; i < health; i++) {
        pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 8 + (i * 8), 8);
        cpct_drawTileAligned2x8_f(hud_heart_full, pvmem);
    }
    
    // Lives
    for (u8 i = 0; i < lives; i++) {
        pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 8 + (i * 8), 16);
        cpct_drawTileAligned2x8_f(hud_life_icon, pvmem);
    }
    
    // Weapon
    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 8, 24);
    cpct_drawTileAligned2x8_f(hud_weapon_icons[player.current_weapon], pvmem);
}