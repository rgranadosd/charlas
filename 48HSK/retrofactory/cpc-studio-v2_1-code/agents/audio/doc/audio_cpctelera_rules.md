# CPCtelera Audio Rules — AY-3-8912 Direct + Arkos Backend

## AY-3-8912 Overview
The Amstrad CPC has an AY-3-8912 PSG (Programmable Sound Generator) with:
- 3 tone channels (A, B, C)
- 1 shared noise channel
- Envelope generator
- 14 registers (R0..R13)

## Direct AY Access via SDCC __sfr (BEEP BACKEND — compilable without .aks)

```c
__sfr __at(0xF4) g_AY_latch;   /* select register: OUT (0xF4), reg */
__sfr __at(0xF6) g_AY_write;   /* write value:     OUT (0xF6), val */

void ay_write(u8 reg, u8 val) {
    g_AY_latch = reg;
    g_AY_write = val;
}
```

## Key AY Registers

| Reg | Function                        | Value range |
|-----|----------------------------------|-------------|
| R0  | Channel A tone period (low)      | 0-255       |
| R1  | Channel A tone period (high)     | 0-15        |
| R2  | Channel B tone period (low)      | 0-255       |
| R3  | Channel B tone period (high)     | 0-15        |
| R4  | Channel C tone period (low)      | 0-255       |
| R5  | Channel C tone period (high)     | 0-15        |
| R6  | Noise period                     | 0-31        |
| R7  | Mixer: bits 5-3=noise C/B/A off, bits 2-0=tone C/B/A off (0=enable) |
| R8  | Channel A volume (0=off, 15=max, bit4=envelope) | 0-15 |
| R9  | Channel B volume                 | 0-15        |
| R10 | Channel C volume                 | 0-15        |
| R11 | Envelope period (low)            | 0-255       |
| R12 | Envelope period (high)           | 0-255       |
| R13 | Envelope shape                   | 0-15        |

## Tone Frequency Formula
tone_period = CPC_clock / (16 * frequency_hz) = 1_000_000 / (16 * freq)
- 440 Hz (A4): period ≈ 142 (0x8E)
- 880 Hz (A5): period ≈ 71  (0x47)
- 1760 Hz:    period ≈ 35  (0x23)

## Audio Interface Contract (ALL games must implement)

```c
/* SFX IDs — extend per game */
#define SFX_WALL_HIT    0
#define SFX_PADDLE_HIT  1
#define SFX_BRICK_HIT   2
#define SFX_LIFE_LOST   3
#define SFX_GAME_OVER   4
#define SFX_LEVEL_CLEAR 5

/* Music track IDs */
#define MUSIC_MAIN      0
#define MUSIC_GAMEOVER  1

void audio_init(void);            /* call once at startup */
void audio_update(void);          /* call every frame in while(1) */
void audio_play_sfx(u8 sfx_id);   /* trigger one-shot SFX */
void audio_start_music(u8 track); /* start background music (no-op in beep backend) */
void audio_stop_all(void);        /* silence all channels */
```

## BEEP BACKEND implementation (default — always compiles)

```c
__sfr __at(0xF4) g_AY_latch;
__sfr __at(0xF6) g_AY_write;

static u8  s_sfx_channel = 0;   /* channel A = 0 */
static u8  s_sfx_vol     = 0;
static u8  s_sfx_timer   = 0;

void audio_init(void) {
    /* Silence all channels */
    g_AY_latch = 8;  g_AY_write = 0;
    g_AY_latch = 9;  g_AY_write = 0;
    g_AY_latch = 10; g_AY_write = 0;
    g_AY_latch = 7;  g_AY_write = 0x3F; /* all off */
}

void audio_update(void) {
    /* Decay active SFX */
    if (s_sfx_timer > 0) {
        s_sfx_timer--;
        if (s_sfx_timer == 0) {
            g_AY_latch = 8; g_AY_write = 0; /* silence channel A */
            g_AY_latch = 7; g_AY_write = 0x3F;
        }
    }
}

void audio_play_sfx(u8 sfx_id) {
    u8 period_lo, period_hi, duration;
    switch (sfx_id) {
        case SFX_WALL_HIT:    period_lo=0x23; period_hi=0; duration=4;  break;
        case SFX_PADDLE_HIT:  period_lo=0x47; period_hi=0; duration=6;  break;
        case SFX_BRICK_HIT:   period_lo=0x8E; period_hi=0; duration=5;  break;
        case SFX_LIFE_LOST:   period_lo=0xFF; period_hi=1; duration=20; break;
        case SFX_GAME_OVER:   period_lo=0xFF; period_hi=3; duration=40; break;
        default:              period_lo=0x47; period_hi=0; duration=4;  break;
    }
    g_AY_latch = 0; g_AY_write = period_lo;
    g_AY_latch = 1; g_AY_write = period_hi;
    g_AY_latch = 7; g_AY_write = 0x3E; /* enable tone on channel A */
    g_AY_latch = 8; g_AY_write = 12;   /* volume */
    s_sfx_timer = duration;
}

void audio_start_music(u8 track_id) {
    (void)track_id; /* BEEP BACKEND: no-op. Replace with Arkos call when .aks available */
}

void audio_stop_all(void) {
    g_AY_latch = 7; g_AY_write = 0x3F;
    g_AY_latch = 8; g_AY_write = 0;
    g_AY_latch = 9; g_AY_write = 0;
    g_AY_latch = 10; g_AY_write = 0;
    s_sfx_timer = 0;
}
```

## ARKOS BACKEND (future — requires .aks compiled binary)

When .aks assets are available, replace audio_init/update/start_music with:
```c
#include "arkos_player.h"   /* provided with CPCtelera Arkos integration */
extern const u8 music_data[];  /* compiled from .aks file */

void audio_init(void)           { InitSound(); }
void audio_update(void)         { PlaySound(); }          /* call every frame */
void audio_start_music(u8 id)   { PlayMusic(music_data); }
void audio_play_sfx(u8 sfx_id)  { PlaySFX(sfx_id, 1, 2); } /* sfx, channel, vol */
void audio_stop_all(void)       { StopSound(); }
```

## Integration points in gameplay
audio_play_sfx() should be called ONLY from update_game(), never from draw_*().
audio_update() goes at the END of the main while(1) loop, after cpct_waitVSYNC().
