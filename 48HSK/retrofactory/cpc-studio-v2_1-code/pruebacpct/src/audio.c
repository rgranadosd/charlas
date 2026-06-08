/* audio.c — Phase 2: direct AY-3-8912 access via Z80 inline assembly.
   CPC AY ports: BC=0xF400 to latch register, BC=0xF600 to write value.
   __sfr __at(0xFx) is WRONG (generates OUT (N),A using A as port high byte).
   Correct approach: OUT (c),A with BC=16-bit port address. */
#include "audio.h"

/* Global relay vars — avoids SDCC Z80 calling-convention issues in inline asm */
static u8 g_ay_reg;
static u8 g_ay_dat;
static u8 g_sfx_timer;

static void ay_write_hw(void) {
    __asm
        ; Phase 1 — latch register address: BDIR=1, BC1=1
        ld  a, (_g_ay_reg)
        ld  bc, #0xF4FF     ; PPI Port A (AY data bus)
        out (c), a           ; put register number on bus
        ld  b, #0xF6
        ld  a, #0xC0         ; BDIR=1 (bit7), BC1=1 (bit6) = LATCH ADDRESS
        out (c), a
        ld  a, #0x40         ; BDIR=0 = inactive
        out (c), a
        ; Phase 2 — write data: BDIR=1, BC1=0
        ld  a, (_g_ay_dat)
        ld  bc, #0xF4FF     ; PPI Port A
        out (c), a           ; put data value on bus
        ld  b, #0xF6
        ld  a, #0x80         ; BDIR=1 (bit7), BC1=0 (bit6) = WRITE DATA
        out (c), a
        ld  a, #0x40         ; BDIR=0 = inactive
        out (c), a
    __endasm;
}

#define AY(r, v) do { g_ay_reg = (r); g_ay_dat = (v); ay_write_hw(); } while(0)

void audio_init(void) {
    g_sfx_timer = 0;
    AY(7,  0x3F);  /* mixer: silence all */
    AY(8,  0);     /* channel A volume = 0 */
    AY(9,  0);     /* channel B volume = 0 */
    AY(10, 0);     /* channel C volume = 0 */
}

void audio_update(void) {
    if (g_sfx_timer > 0) {
        g_sfx_timer--;
        if (g_sfx_timer == 0) {
            AY(8, 0);       /* silence channel A */
            AY(7, 0x3F);    /* mixer off */
        }
    }
}

void audio_play_sfx(u8 sfx_id) {
    u8 period_lo, duration;
    switch (sfx_id) {
        case SFX_WALL_HIT:   period_lo = 0x23; duration = 4;  break;
        case SFX_PADDLE_HIT: period_lo = 0x47; duration = 6;  break;
        case SFX_BRICK_HIT:  period_lo = 0x8E; duration = 5;  break;
        case SFX_LIFE_LOST:  period_lo = 0xFF; duration = 20; break;
        case SFX_GAME_OVER:  period_lo = 0xCC; duration = 40; break;
        default: return;
    }
    AY(0, period_lo);  /* tone period channel A low */
    AY(1, 0);          /* tone period channel A high */
    AY(7, 0x3E);       /* enable tone on channel A */
    AY(8, 12);         /* channel A volume */
    g_sfx_timer = duration;
}
