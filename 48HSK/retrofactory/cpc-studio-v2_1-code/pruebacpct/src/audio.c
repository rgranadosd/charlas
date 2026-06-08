#include "audio.h"

static u8 g_ay_reg;
static u8 g_ay_dat;
static u8 g_sfx_timer;

static void ay_write_hw(void) {
    __asm
        ld  a, (_g_ay_reg)
        ld  bc, #0xF4FF
        out (c), a
        ld  b, #0xF6
        ld  a, #0xC0
        out (c), a
        ld  a, #0x40
        out (c), a
        ld  a, (_g_ay_dat)
        ld  bc, #0xF4FF
        out (c), a
        ld  b, #0xF6
        ld  a, #0x80
        out (c), a
        ld  a, #0x40
        out (c), a
    __endasm;
}

#define AY(r, v) do { g_ay_reg = (r); g_ay_dat = (v); ay_write_hw(); } while (0)

void audio_init(void) {
    g_sfx_timer = 0;
    AY(7, 0x3F);
    AY(8, 0);
    AY(9, 0);
    AY(10, 0);
}

void audio_update(void) {
    if (g_sfx_timer > 0) {
        g_sfx_timer--;
        if (g_sfx_timer == 0) {
            AY(8, 0);
            AY(7, 0x3F);
        }
    }
}

void audio_play_sfx(u8 sfx_id) {
    u8 period_lo;
    u8 duration;

    switch (sfx_id) {
        case SFX_WALL_HIT:   period_lo = 0x23; duration = 4;  break;
        case SFX_PADDLE_HIT: period_lo = 0x47; duration = 6;  break;
        case SFX_BRICK_HIT:  period_lo = 0x8E; duration = 5;  break;
        case SFX_LIFE_LOST:  period_lo = 0xFF; duration = 20; break;
        case SFX_GAME_OVER:  period_lo = 0xCC; duration = 40; break;
        default: return;
    }

    AY(0, period_lo);
    AY(1, 0);
    AY(7, 0x3E);
    AY(8, 12);
    g_sfx_timer = duration;
}