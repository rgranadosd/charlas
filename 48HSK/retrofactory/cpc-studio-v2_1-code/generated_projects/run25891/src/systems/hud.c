#include "hud.h"
#include "../entities/player.h"
#include <cpctelera.h>

const u8 heart_sprite[8*8/8] = { /* Sprite data */ };
const u8 armor_sprite[8*8/8] = { /* Sprite data */ };
const u8 dagger_sprite[8*8/8] = { /* Sprite data */ };

u16 score = 0;

u8 score_digits[6] = {0};

u8* const score_positions[6] = {
    (u8*)0xC000 + 40*8 + 8*2,
    (u8*)0xC000 + 40*8 + 8*3,
    (u8*)0xC000 + 40*8 + 8*4,
    (u8*)0xC000 + 40*8 + 8*5,
    (u8*)0xC000 + 40*8 + 8*6,
    (u8*)0xC000 + 40*8 + 8*7
};

extern const u8 font[96][8];

void hud_init(void) {
    score = 0;
    hud_update_score(0);
}

void hud_update_score(u16 new_score) {
    score = new_score;
    for (u8 i = 0; i < 6; i++) {
        score_digits[i] = score % 10;
        score /= 10;
    }
}

void hud_draw(void) {
    // Draw health
    for (u8 i = 0; i < player.health; i++) {
        cpct_drawSprite(heart_sprite, (u8*)0xC000 + 40*8 + 8*i, 8, 8);
    }
    
    // Draw lives
    for (u8 i = 0; i < player.lives; i++) {
        cpct_drawSprite(armor_sprite, (u8*)0xC000 + 8*i, 8, 8);
    }
    
    // Draw ammo
    cpct_drawSprite(dagger_sprite, (u8*)0xC000 + 8*18, 8, 8);
    cpct_drawCharM0((u8*)0xC000 + 8*19, '0' + player.ammo);
    
    // Draw score
    for (u8 i = 0; i < 6; i++) {
        cpct_drawCharM0(score_positions[5-i], '0' + score_digits[i]);
    }
}