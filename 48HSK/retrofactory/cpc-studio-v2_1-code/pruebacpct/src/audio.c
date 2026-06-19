#include "audio.h"

static u8 g_ay_reg;
static u8 g_ay_dat;
static u8 s_sfx_timer;

static void ay_write_hw(void) {
    __asm
        ; Fase 1 — latch del registro: BDIR=1, BC1=1
        ld  a, (_g_ay_reg)
        ld  bc, #0xF4FF
        out (c), a
        ld  b, #0xF6
        ld  a, #0xC0
        out (c), a
        ld  a, #0x40
        out (c), a
        ; Fase 2 — escritura del dato: BDIR=1, BC1=0
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

#define AY(r, v) do { g_ay_reg = (r); g_ay_dat = (v); ay_write_hw(); } while(0)

void audio_init(void) {
    // Silenciar todo
    AY(7, 0x3F);  // Mixer: todo apagado
    AY(8, 0);    // Volumen canal A: 0
    s_sfx_timer = 0;
}

void audio_update(void) {
    if (s_sfx_timer > 0) {
        s_sfx_timer--;
        if (s_sfx_timer == 0) {
            // Silenciar al terminar el SFX
            AY(8, 0);    // Volumen canal A: 0
            AY(7, 0x3F);  // Mixer: todo apagado
        }
    }
}

void audio_play_sfx(u8 sfx_id) {
    u8 period_low, period_high, duration;

    switch (sfx_id) {
        case SFX_WALL_HIT:
            period_low = 35;    // 1760 Hz (agudo)
            period_high = 0;
            duration = 4;
            break;
        case SFX_PADDLE_HIT:
            period_low = 71;    // 880 Hz (medio)
            period_high = 0;
            duration = 5;
            break;
        case SFX_BRICK_HIT:
            period_low = 142;   // 440 Hz (grave)
            period_high = 0;
            duration = 6;
            break;
        case SFX_LIFE_LOST:
            period_low = 142;   // 440 Hz (grave)
            period_high = 0;
            duration = 20;
            break;
        case SFX_GAME_OVER:
            period_low = 142;   // 440 Hz (grave)
            period_high = 0;
            duration = 40;
            break;
        default:
            return;
    }

    // Configurar y reproducir el SFX
    AY(0, period_low);
    AY(1, period_high);
    AY(7, 0x3E);      // Habilitar tono canal A
    AY(8, 12);       // Volumen canal A: 12
    s_sfx_timer = duration;
}